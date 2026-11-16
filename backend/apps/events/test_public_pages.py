import json
from datetime import timedelta
from xml.etree import ElementTree

from django.test import TestCase, override_settings
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Audience, Place
from apps.events.models import Event, EventScheduleItem


@override_settings(
    ALLOWED_HOSTS=['testserver', 'radarcultural.mx'],
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class PublicEventPageTests(TestCase):
    def setUp(self):
        editor = User.objects.create_user(
            username='page-editor',
            email='page-editor@example.test',
            password='not-a-production-password',
        )
        self.event = Event(
            title='Festival de prueba',
            summary='Una experiencia cultural verificada.',
            description='Consulta el programa y la fuente.',
            starts_at=timezone.now() + timedelta(days=2),
            time_zone='America/Mexico_City',
            attendance_mode=Event.ATTENDANCE_ONLINE,
            online_url='https://example.test/transmision',
            external_organizer_name='Colectivo de prueba',
            source_url='https://example.test/fuente',
            created_by=editor,
            publication_status=Event.PUBLICATION_PUBLISHED,
        )
        self.event.full_clean()
        self.event.save()

    def test_published_page_has_server_rendered_metadata_and_schema(self):
        response = self.client.get(
            f'/eventos/{self.event.slug}/',
            secure=True,
            HTTP_HOST='radarcultural.mx',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response['Content-Type'])
        self.assertEqual(response['Cache-Control'], 'no-store')
        self.assertContains(response, '<h1>Festival de prueba</h1>', html=True)
        self.assertContains(
            response,
            f'<link rel="canonical" href="https://radarcultural.mx/eventos/{self.event.slug}/">',
            html=True,
        )
        self.assertNotContains(response, 'page-editor@example.test')
        html = response.content.decode()
        payload = html.split('<script type="application/ld+json">', 1)[1].split('</script>', 1)[0]
        schema = json.loads(payload)
        self.assertEqual(schema['@type'], 'Event')
        self.assertEqual(schema['name'], self.event.title)
        self.assertEqual(schema['url'], f'https://radarcultural.mx/eventos/{self.event.slug}/')
        self.assertContains(response, 'Zona del evento: America/Mexico_City')

    def test_draft_hidden_and_removed_pages_return_http_404(self):
        for publication_status, visibility_status in (
            (Event.PUBLICATION_DRAFT, Event.VISIBILITY_PUBLIC),
            (Event.PUBLICATION_PUBLISHED, Event.VISIBILITY_HIDDEN),
            (Event.PUBLICATION_PUBLISHED, Event.VISIBILITY_REMOVED),
        ):
            with self.subTest(status=(publication_status, visibility_status)):
                self.event.publication_status = publication_status
                self.event.visibility_status = visibility_status
                self.event.save()
                response = self.client.get(f'/eventos/{self.event.slug}/')
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response['Cache-Control'], 'no-store')

    def test_structured_data_cannot_close_its_script_element(self):
        self.event.title = '</script><script>alert(1)</script>'
        self.event.save()
        response = self.client.get(f'/eventos/{self.event.slug}/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertEqual(html.count('</script>'), 3)
        self.assertIn(r'\u003C/script\u003E', html)
        self.assertNotIn('<script>alert(1)</script>', html)

    def test_unlicensed_image_is_not_rendered(self):
        self.event.image_url = 'https://example.test/photo.jpg'
        self.event.image_license = Event.IMAGE_ALL_RIGHTS
        self.event.save()
        response = self.client.get(f'/eventos/{self.event.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'https://example.test/photo.jpg')

    def test_recorded_permission_has_no_invented_license_or_inventory_in_html(self):
        self.event.description_license = Event.DESCRIPTION_PERMISSION
        self.event.save(update_fields=['description_license', 'updated_at'])
        response = self.client.get(f'/eventos/{self.event.slug}/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        payload = html.split('<script type="application/ld+json">', 1)[1].split('</script>', 1)[0]
        schema = json.loads(payload)
        self.assertNotIn('license', schema)
        self.assertNotIn('availability', schema['offers'][0])
        self.assertNotIn('licencia-permiso-registrado', html)

    def test_detail_displays_program_audience_country_and_paid_options(self):
        place = Place.objects.create(name='Sala de prueba', locality='Paris', country_code='FR')
        audience = Audience.objects.create(name='Público internacional')
        self.event.place = place
        self.event.attendance_mode = Event.ATTENDANCE_MIXED
        self.event.ends_at = self.event.starts_at + timedelta(hours=3)
        self.event.admission_type = Event.ADMISSION_PAID
        self.event.admission_options = [
            {
                'name': 'Tarifa general',
                'price': '12.50',
                'price_currency': 'EUR',
                'url': 'https://example.test/entradas',
            }
        ]
        self.event.links = [{'label': 'Programa oficial', 'url': 'https://example.test/programa'}]
        self.event.full_clean()
        self.event.save()
        self.event.audiences.add(audience)
        EventScheduleItem.objects.create(
            event=self.event,
            title='Sesión principal',
            starts_at=self.event.starts_at + timedelta(hours=1),
            ends_at=self.event.starts_at + timedelta(hours=2),
        )

        response = self.client.get(f'/eventos/{self.event.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Público internacional')
        self.assertContains(response, 'Sesión principal')
        self.assertContains(response, 'Programa oficial ↗')
        self.assertContains(response, 'Paris, FR')
        self.assertContains(response, 'Tarifa general · 12.50 EUR')
        self.assertContains(response, 'https://example.test/entradas')

    def test_sitemap_lists_only_public_events_and_excludes_legal_drafts(self):
        index = self.client.get('/sitemap.xml', HTTP_HOST='radarcultural.mx')
        self.assertEqual(index.status_code, 200)
        self.assertEqual(index['Cache-Control'], 'no-store')
        self.assertContains(index, 'https://radarcultural.mx/sitemap-events.xml')
        self.assertContains(index, 'https://radarcultural.mx/sitemap-static.xml')

        events = self.client.get('/sitemap-events.xml', HTTP_HOST='radarcultural.mx')
        self.assertEqual(events.status_code, 200)
        self.assertEqual(events['Cache-Control'], 'no-store')
        root = ElementTree.fromstring(events.content)
        namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locations = [node.text for node in root.findall('s:url/s:loc', namespace)]
        self.assertEqual(locations, [f'https://radarcultural.mx/eventos/{self.event.slug}/'])

        static = self.client.get('/sitemap-static.xml', HTTP_HOST='radarcultural.mx')
        self.assertEqual(static.status_code, 200)
        self.assertEqual(static['Cache-Control'], 'no-store')
        self.assertNotIn(b'/privacidad/', static.content)
        self.assertNotIn(b'/terminos/', static.content)

        self.event.visibility_status = Event.VISIBILITY_REMOVED
        self.event.save(update_fields=['visibility_status', 'updated_at'])
        removed = self.client.get('/sitemap-events.xml', HTTP_HOST='radarcultural.mx')
        self.assertEqual(removed.status_code, 200)
        self.assertEqual(removed['Cache-Control'], 'no-store')
        self.assertNotIn(self.event.slug.encode(), removed.content)
