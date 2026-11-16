from datetime import timedelta
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import OrganizationProfile, User
from apps.catalog.models import Audience, Category, Place
from apps.events.models import Event, EventScheduleItem


class PublicApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='api-editor',
            email='api-editor@example.test',
            password='not-a-production-password',
        )
        self.organization_user = User.objects.create_user(
            username='organizacion-api',
            email='organizacion-api@example.test',
            password='not-a-production-password',
            account_type=User.ACCOUNT_ORGANIZATION,
        )
        self.organization = OrganizationProfile.objects.create(
            user=self.organization_user,
            official_name='Organización cultural verificada',
            description='Descripción pública para pruebas.',
            website='https://organizacion.example.test/',
            contact_email='contacto@example.test',
            is_verified=True,
        )
        self.category = Category.objects.create(name='Artes escénicas')
        self.audience = Audience.objects.create(name='Público general')
        self.place = Place.objects.create(
            name='Foro de prueba', locality='Puebla', country_code='MX'
        )
        self.published = self.create_event('Evento publicado', Event.PUBLICATION_PUBLISHED)
        self.draft = self.create_event('Evento privado', Event.PUBLICATION_DRAFT)

    def create_event(self, title, publication_status):
        event = Event(
            title=title,
            summary=f'Resumen de {title}',
            description=f'Descripción de {title}',
            starts_at=timezone.now() + timedelta(days=4),
            time_zone='America/Mexico_City',
            place=self.place,
            organizer=self.organization,
            source_url='https://example.test/fuente',
            created_by=self.user,
            publication_status=publication_status,
        )
        event.full_clean()
        event.save()
        event.categories.add(self.category)
        event.audiences.add(self.audience)
        EventScheduleItem.objects.create(
            event=event,
            title='Apertura',
            starts_at=event.starts_at,
            position=0,
        )
        return event

    def test_status_is_public_and_minimal(self):
        response = self.client.get('/api/v1/status/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'status': 'ok', 'service': 'radar-cultural-api', 'version': 'v1'},
        )

    def test_list_exposes_only_published_events(self):
        response = self.client.get('/api/v1/events/')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body['count'], 1)
        self.assertEqual(body['results'][0]['slug'], self.published.slug)
        self.assertNotIn('created_by', body['results'][0])
        self.assertNotIn('published_by', body['results'][0])
        self.assertNotIn('publication_status', body['results'][0])
        self.assertTrue(body['results'][0]['schema_url'].endswith('/schema/'))
        self.assertTrue(body['results'][0]['rdf_url'].endswith('/schema.rdf'))
        self.assertTrue(body['results'][0]['calendar_url'].endswith('/calendar.ics'))

    @override_settings(ALLOWED_HOSTS=['radarcultural.mx', 'www.radarcultural.mx'])
    def test_absolute_urls_ignore_client_forwarded_host(self):
        response = self.client.get(
            f'/api/v1/events/{self.published.slug}/',
            HTTP_HOST='radarcultural.mx',
            HTTP_X_FORWARDED_HOST='www.radarcultural.mx',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['schema_url'].startswith('http://radarcultural.mx/'))

    def test_legacy_json_extra_keys_never_leave_public_api(self):
        Event.objects.filter(pk=self.published.pk).update(
            admission_type=Event.ADMISSION_PAID,
            admission_options=[
                {
                    'name': 'General',
                    'price': '12.50',
                    'price_currency': 'EUR',
                    'url': 'https://example.test/entradas',
                    'internal_token': 'secreto-no-publico',
                },
                {
                    'name': 'Registro heredado inválido',
                    'price': {'internal_token': 'secreto-anidado'},
                    'price_currency': 'EUR',
                },
                {'name': 'Precio no finito', 'price': 'NaN', 'price_currency': 'EUR'},
                {'name': 'Moneda inválida', 'price': '12', 'price_currency': 'EURO'},
            ],
            links=[
                {
                    'label': 'Programa',
                    'url': 'https://example.test/programa',
                    'private_email': 'contacto-privado@example.test',
                },
                {
                    'label': {'private_email': 'otro-privado@example.test'},
                    'url': 'https://example.test/',
                },
                {'label': 'Enlace inválido', 'url': 'javascript:alert(1)'},
            ],
        )
        for path in ('/api/v1/events/', f'/api/v1/events/{self.published.slug}/'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                event = (
                    response.json()['results'][0] if path.endswith('/events/') else response.json()
                )
                self.assertEqual(
                    event['admission_options'],
                    [
                        {
                            'name': 'General',
                            'price': '12.50',
                            'price_currency': 'EUR',
                            'url': 'https://example.test/entradas',
                        }
                    ],
                )
                self.assertEqual(
                    event['links'],
                    [{'label': 'Programa', 'url': 'https://example.test/programa'}],
                )
                self.assertNotIn('secreto-no-publico', response.content.decode())
                self.assertNotIn('secreto-anidado', response.content.decode())
                self.assertNotIn('contacto-privado@example.test', response.content.decode())
                self.assertNotIn('otro-privado@example.test', response.content.decode())
                self.assertNotIn('javascript:alert(1)', response.content.decode())

        for path in (
            f'/api/v1/events/{self.published.slug}/schema/',
            f'/api/v1/events/{self.published.slug}/schema.rdf',
            f'/eventos/{self.published.slug}/',
        ):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                body = response.content.decode()
                for private_value in (
                    'secreto-no-publico',
                    'secreto-anidado',
                    'contacto-privado@example.test',
                    'otro-privado@example.test',
                    'javascript:alert(1)',
                ):
                    self.assertNotIn(private_value, body)
                if path.endswith('/schema/'):
                    self.assertEqual(len(response.json()['offers']), 1)
                    self.assertEqual(response.json()['offers'][0]['price'], '12.50')
                if path.startswith('/eventos/'):
                    self.assertContains(response, 'General · 12.50 EUR')

    def test_invalid_legacy_paid_options_do_not_break_public_representations(self):
        Event.objects.filter(pk=self.published.pk).update(
            admission_type=Event.ADMISSION_PAID,
            admission_options=[{'name': 'Mal formado', 'price': 'NaN', 'price_currency': 'EUR'}],
        )
        detail = self.client.get(f'/api/v1/events/{self.published.slug}/')
        schema = self.client.get(f'/api/v1/events/{self.published.slug}/schema/')
        html = self.client.get(f'/eventos/{self.published.slug}/')
        for response in (detail, schema, html):
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('NaN', response.content.decode())
        self.assertEqual(detail.json()['admission_options'], [])
        self.assertEqual(schema.json()['offers'], [])
        self.assertContains(html, 'Consulta las opciones en la fuente.')

    def test_draft_detail_is_not_discoverable(self):
        response = self.client.get(f'/api/v1/events/{self.draft.slug}/')
        self.assertEqual(response.status_code, 404)

    def test_event_representations_are_not_stored_after_withdrawal(self):
        paths = (
            '/api/v1/events/',
            f'/api/v1/events/{self.published.slug}/',
            f'/api/v1/events/{self.published.slug}/schema/',
            f'/api/v1/events/{self.published.slug}/schema.rdf',
            f'/api/v1/events/{self.published.slug}/calendar.ics',
        )
        for path in paths:
            with self.subTest(path=path, publication='public'):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['Cache-Control'], 'no-store')

        self.published.visibility_status = Event.VISIBILITY_REMOVED
        self.published.save(update_fields=['visibility_status', 'updated_at'])
        for path in paths:
            with self.subTest(path=path, publication='removed'):
                response = self.client.get(path)
                self.assertEqual(response['Cache-Control'], 'no-store')
                if path == '/api/v1/events/':
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()['count'], 0)
                else:
                    self.assertEqual(response.status_code, 404)

    def test_public_api_rejects_writes_even_when_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/v1/events/', {'title': 'No permitido'}, format='json')
        self.assertEqual(response.status_code, 405)

    def test_filters_by_category_and_query(self):
        category_response = self.client.get('/api/v1/events/', {'category': self.category.slug})
        search_response = self.client.get('/api/v1/events/', {'q': 'publicado'})
        missing_response = self.client.get('/api/v1/events/', {'q': 'inexistente'})
        self.assertEqual(category_response.json()['count'], 1)
        self.assertEqual(search_response.json()['count'], 1)
        self.assertEqual(missing_response.json()['count'], 0)

    def test_invalid_date_returns_structured_error(self):
        response = self.client.get('/api/v1/events/', {'from': 'no-es-fecha'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'La solicitud contiene parámetros inválidos.')
        self.assertIn('from', response.json()['errors'])

    def test_date_filters_require_explicit_timezone(self):
        for field in ('from', 'to', 'updated_since'):
            with self.subTest(field=field):
                response = self.client.get('/api/v1/events/', {field: '2026-11-08T12:00:00'})
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json()['errors'])

    def test_date_filters_compare_instants_across_offsets(self):
        instant = self.published.starts_at
        after = (instant + timedelta(minutes=1)).astimezone(timezone.get_fixed_timezone(-300))
        before = (instant - timedelta(minutes=1)).astimezone(timezone.get_fixed_timezone(60))
        included = self.client.get(
            '/api/v1/events/',
            {'from': before.isoformat(), 'to': after.isoformat()},
        )
        excluded = self.client.get('/api/v1/events/', {'from': after.isoformat()})
        self.assertEqual(included.status_code, 200)
        self.assertEqual(included.json()['count'], 1)
        self.assertEqual(excluded.status_code, 200)
        self.assertEqual(excluded.json()['count'], 0)

    def test_not_finished_filter_includes_ongoing_and_future_program_activities(self):
        instant = timezone.now()
        ongoing = self.create_event('Evento en curso', Event.PUBLICATION_PUBLISHED)
        ongoing.starts_at = instant - timedelta(hours=2)
        ongoing.ends_at = instant + timedelta(hours=2)
        ongoing.save(update_fields=['starts_at', 'ends_at', 'updated_at'])
        ongoing.schedule_items.update(starts_at=ongoing.starts_at)

        program = self.create_event('Programa con actividad futura', Event.PUBLICATION_PUBLISHED)
        program.starts_at = instant - timedelta(days=2)
        program.save(update_fields=['starts_at', 'updated_at'])
        program.schedule_items.update(starts_at=instant + timedelta(days=1))

        ongoing_program = self.create_event(
            'Programa con actividad en curso', Event.PUBLICATION_PUBLISHED
        )
        ongoing_program.starts_at = instant - timedelta(days=2)
        ongoing_program.ends_at = None
        ongoing_program.save(update_fields=['starts_at', 'ends_at', 'updated_at'])
        ongoing_program.schedule_items.update(
            starts_at=instant - timedelta(hours=1),
            ends_at=instant + timedelta(hours=1),
        )

        ended = self.create_event('Evento terminado', Event.PUBLICATION_PUBLISHED)
        ended.starts_at = instant - timedelta(days=2)
        ended.ends_at = instant - timedelta(days=1)
        ended.save(update_fields=['starts_at', 'ends_at', 'updated_at'])
        ended.schedule_items.update(starts_at=ended.starts_at)

        cancelled = self.create_event('Evento cancelado', Event.PUBLICATION_PUBLISHED)
        cancelled.event_status = Event.STATUS_CANCELLED
        cancelled.save(update_fields=['event_status', 'updated_at'])

        response = self.client.get(
            '/api/v1/events/',
            {'not_finished_at': instant.isoformat(), 'status': Event.STATUS_SCHEDULED},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {item['slug'] for item in response.json()['results']},
            {self.published.slug, ongoing.slug, program.slug, ongoing_program.slug},
        )
        starts_only = self.client.get(
            '/api/v1/events/',
            {'from': instant.isoformat(), 'status': Event.STATUS_SCHEDULED},
        )
        self.assertEqual(
            {item['slug'] for item in starts_only.json()['results']}, {self.published.slug}
        )
        invalid = self.client.get('/api/v1/events/', {'not_finished_at': '2026-11-09T12:00:00'})
        self.assertEqual(invalid.status_code, 400)
        self.assertIn('not_finished_at', invalid.json()['errors'])

    def test_reversed_date_range_is_rejected(self):
        instant = self.published.starts_at
        response = self.client.get(
            '/api/v1/events/',
            {
                'from': (instant + timedelta(minutes=1)).isoformat(),
                'to': (instant - timedelta(minutes=1)).isoformat(),
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('to', response.json()['errors'])

    def test_invalid_place_returns_structured_error(self):
        response = self.client.get('/api/v1/events/', {'place': 'no-es-uuid'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'La solicitud contiene parámetros inválidos.')
        self.assertIn('place', response.json()['errors'])

    def test_image_filter_matches_only_public_reusable_images(self):
        for event in (self.published, self.draft):
            event.image_url = 'https://example.test/imagen.jpg'
            event.image_license = Event.IMAGE_CC_BY
            event.image_credit = 'Archivo de prueba'
            event.image_source_url = 'https://example.test/origen'
            event.include_image_in_open_data = True
            event.full_clean()
            event.save()
        with_image = self.client.get('/api/v1/events/', {'has_image': 'true'})
        without_image = self.client.get('/api/v1/events/', {'has_image': 'false'})
        invalid = self.client.get('/api/v1/events/', {'has_image': 'yes'})
        self.assertEqual(with_image.status_code, 200)
        self.assertEqual(with_image.json()['count'], 1)
        self.assertEqual(with_image.json()['results'][0]['slug'], self.published.slug)
        self.assertIsNotNone(with_image.json()['results'][0]['image'])
        self.assertEqual(without_image.status_code, 200)
        self.assertEqual(without_image.json()['count'], 0)
        self.assertEqual(invalid.status_code, 400)
        self.assertIn('has_image', invalid.json()['errors'])

    def test_event_filter_inputs_are_bounded(self):
        cases = (
            ('category', 'a' * 181),
            ('audience', 'a' * 181),
            ('organizer', 'a' * 281),
            ('category', '文化'),
            ('place', 'f' * 37),
            ('from', '2' * 65),
            ('not_finished_at', '2' * 65),
            ('to', '2' * 65),
            ('updated_since', '2' * 65),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value[:20]):
                response = self.client.get('/api/v1/events/', {field: value})
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json()['errors'])

    def test_catalogs_are_paginated_and_inactive_rows_are_hidden(self):
        Category.objects.create(name='Oculta', is_active=False)
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_invalid_catalog_identifiers_do_not_raise_server_errors(self):
        for resource in ('categories', 'audiences', 'places'):
            with self.subTest(resource=resource):
                response = self.client.get(f'/api/v1/{resource}/not-a-uuid/')
                self.assertEqual(response.status_code, 404)

    def test_verified_organizations_are_public_and_unverified_ones_are_hidden(self):
        hidden_user = User.objects.create_user(
            username='organizacion-oculta',
            email='organizacion-oculta@example.test',
            password='not-a-production-password',
            account_type=User.ACCOUNT_ORGANIZATION,
        )
        OrganizationProfile.objects.create(
            user=hidden_user,
            official_name='Organización sin verificar',
            contact_email='privado@example.test',
        )
        response = self.client.get('/api/v1/organizations/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        organization = response.json()['results'][0]
        self.assertEqual(organization['slug'], self.organization.slug)
        self.assertNotIn('contact_email', organization)

    def test_revoked_organization_is_not_cached_or_discoverable(self):
        path = f'/api/v1/organizations/{self.organization.slug}/'
        visible = self.client.get(path)
        self.assertEqual(visible.status_code, 200)
        self.assertEqual(visible['Cache-Control'], 'no-store')

        self.organization.is_verified = False
        self.organization.save(update_fields=['is_verified', 'updated_at'])
        missing = self.client.get(path)
        listing = self.client.get('/api/v1/organizations/')
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(missing['Cache-Control'], 'no-store')
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing['Cache-Control'], 'no-store')
        self.assertEqual(listing.json()['count'], 0)

    def test_unverified_event_organizer_exposes_only_its_public_name(self):
        hidden_user = User.objects.create_user(
            username='organizacion-evento-no-verificada',
            email='organizacion-evento-no-verificada@example.test',
            password='not-a-production-password',
            account_type=User.ACCOUNT_ORGANIZATION,
        )
        hidden = OrganizationProfile.objects.create(
            user=hidden_user,
            official_name='Organización pendiente',
            description='No debe publicarse antes de la verificación.',
            website='https://privado.example.test/',
            contact_email='privado@example.test',
        )
        self.published.organizer = hidden
        self.published.save(update_fields=['organizer', 'updated_at'])
        response = self.client.get(f'/api/v1/events/{self.published.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['organizer'], {'name': hidden.official_name})
        filtered = self.client.get('/api/v1/events/', {'organizer': hidden.slug})
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(filtered.json()['count'], 0)

    def test_schema_endpoint_is_public_and_uses_the_canonical_event_mapping(self):
        response = self.client.get(
            f'/api/v1/events/{self.published.slug}/schema/',
            HTTP_ACCEPT='application/ld+json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/ld+json')
        body = response.json()
        self.assertEqual(body['@context'], 'https://schema.org')
        self.assertEqual(body['@type'], 'Event')
        self.assertEqual(body['@id'], f'urn:uuid:{self.published.id}')
        self.assertEqual(body['url'], f'http://testserver/eventos/{self.published.slug}/')
        self.assertEqual(body['organizer']['name'], self.organization.official_name)
        self.assertEqual(body['location']['name'], self.place.name)
        self.assertEqual(body['offers'][0]['price'], '0')
        self.assertNotIn('availability', body['offers'][0])
        self.assertNotIn('created_by', body)

    def test_recorded_permission_does_not_claim_a_public_license_or_ticket_inventory(self):
        self.published.description_license = Event.DESCRIPTION_PERMISSION
        self.published.admission_type = Event.ADMISSION_PAID
        self.published.admission_options = [
            {'name': 'General', 'price': '100', 'price_currency': 'MXN'}
        ]
        self.published.full_clean()
        self.published.save()

        detail = self.client.get(f'/api/v1/events/{self.published.slug}/')
        schema = self.client.get(f'/api/v1/events/{self.published.slug}/schema/')
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(schema.status_code, 200)
        self.assertEqual(detail.json()['description_license'], Event.DESCRIPTION_PERMISSION)
        self.assertIsNone(detail.json()['license_url'])
        self.assertNotIn('license', schema.json())
        self.assertEqual(schema.json()['offers'][0]['priceCurrency'], 'MXN')
        self.assertNotIn('availability', schema.json()['offers'][0])

    def test_event_language_and_free_offer_do_not_assume_mexico(self):
        detail = self.client.get(f'/api/v1/events/{self.published.slug}/')
        schema = self.client.get(f'/api/v1/events/{self.published.slug}/schema/')
        self.assertIsNone(detail.json()['language_code'])
        self.assertNotIn('inLanguage', schema.json())
        self.assertNotIn('priceCurrency', schema.json()['offers'][0])

        self.published.language_code = 'en-US'
        self.published.save(update_fields=['language_code', 'updated_at'])
        detail = self.client.get(f'/api/v1/events/{self.published.slug}/')
        schema = self.client.get(f'/api/v1/events/{self.published.slug}/schema/')
        self.assertEqual(detail.json()['language_code'], 'en-US')
        self.assertEqual(schema.json()['inLanguage'], 'en-US')

    def test_event_time_zone_is_explicit_in_api_and_schema(self):
        self.published.time_zone = 'Europe/Paris'
        self.published.save(update_fields=['time_zone', 'updated_at'])
        detail = self.client.get(f'/api/v1/events/{self.published.slug}/')
        schema = self.client.get(f'/api/v1/events/{self.published.slug}/schema/')
        self.assertEqual(detail.json()['time_zone'], 'Europe/Paris')
        self.assertEqual(
            schema.json()['startDate'],
            self.published.starts_at.astimezone(ZoneInfo('Europe/Paris')).isoformat(),
        )

    def test_draft_has_no_schema_or_calendar_representation(self):
        schema_response = self.client.get(f'/api/v1/events/{self.draft.slug}/schema/')
        rdf_response = self.client.get(f'/api/v1/events/{self.draft.slug}/schema.rdf')
        calendar_response = self.client.get(f'/api/v1/events/{self.draft.slug}/calendar.ics')
        self.assertEqual(schema_response.status_code, 404)
        self.assertEqual(rdf_response.status_code, 404)
        self.assertEqual(calendar_response.status_code, 404)

    def test_rdf_endpoint_matches_the_public_schema_mapping(self):
        response = self.client.get(
            f'/api/v1/events/{self.published.slug}/schema.rdf',
            HTTP_ACCEPT='application/rdf+xml',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('application/rdf+xml'))
        root = ElementTree.fromstring(response.content)
        namespace = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'schema': 'https://schema.org/',
        }
        event = root.find('schema:Event', namespace)
        self.assertIsNotNone(event)
        self.assertEqual(event.find('schema:name', namespace).text, self.published.title)
        organizer = event.find(
            'schema:organizer/schema:Organization/schema:name',
            namespace,
        )
        self.assertEqual(organizer.text, self.organization.official_name)

    def test_calendar_endpoint_returns_a_stable_ical_event(self):
        response = self.client.get(
            f'/api/v1/events/{self.published.slug}/calendar.ics',
            HTTP_ACCEPT='text/calendar',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('text/calendar'))
        content = response.content.decode()
        self.assertIn('BEGIN:VCALENDAR', content)
        self.assertIn(f'UID:{self.published.id}@radarcultural.mx', content)
        self.assertIn('SUMMARY:Evento publicado', content)
        self.assertIn(r'LOCATION:Foro de prueba\, Puebla\, MX', content)
        self.assertIn('END:VCALENDAR', content)

    def test_hybrid_calendar_includes_country_and_online_access(self):
        self.place.region = 'Puebla'
        self.place.address = 'Calle de prueba 12'
        self.place.save()
        self.published.attendance_mode = Event.ATTENDANCE_MIXED
        self.published.online_url = 'https://example.test/transmision'
        self.published.location_details = 'Sala A'
        self.published.full_clean()
        self.published.save()

        response = self.client.get(f'/api/v1/events/{self.published.slug}/calendar.ics')
        self.assertEqual(response.status_code, 200)
        logical_lines = response.content.decode('utf-8').replace('\r\n ', '').split('\r\n')
        self.assertIn(
            r'LOCATION:Foro de prueba\, Sala A\, Calle de prueba 12\, Puebla\, MX',
            logical_lines,
        )
        self.assertTrue(
            any(
                r'Acceso en línea: https://example.test/transmision' in line
                for line in logical_lines
            )
        )

    def test_calendar_folds_utf8_and_escapes_untrusted_line_breaks(self):
        self.published.title = '文化' * 40 + ';,\\\rATTENDEE:intruso@example.test'
        self.published.summary = 'Primera línea\r\nSEGUNDA: línea\rTERCERA: línea'
        self.published.save(update_fields=['title', 'summary', 'updated_at'])

        response = self.client.get(f'/api/v1/events/{self.published.slug}/calendar.ics')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertTrue(content.endswith('\r\n'))
        self.assertTrue(all(len(line.encode('utf-8')) <= 75 for line in content.split('\r\n')))

        logical_lines = content.replace('\r\n ', '').split('\r\n')
        self.assertEqual(sum(line.startswith('SUMMARY:') for line in logical_lines), 1)
        self.assertFalse(
            any(line.startswith(('ATTENDEE:', 'SEGUNDA:', 'TERCERA:')) for line in logical_lines)
        )
        self.assertTrue(
            any(r'\;\,\\\nATTENDEE:intruso@example.test' in line for line in logical_lines)
        )
        self.assertTrue(
            any(r'Primera línea\nSEGUNDA: línea\nTERCERA: línea' in line for line in logical_lines)
        )

    def test_semantic_representations_support_head_and_options(self):
        endpoints = (
            (f'/api/v1/events/{self.published.slug}/schema/', 'application/ld+json'),
            (f'/api/v1/events/{self.published.slug}/schema.rdf', 'application/rdf+xml'),
            (f'/api/v1/events/{self.published.slug}/calendar.ics', 'text/calendar'),
        )
        for path, content_type in endpoints:
            with self.subTest(path=path):
                head = self.client.head(path, HTTP_ACCEPT=content_type)
                options = self.client.options(path)
                self.assertEqual(head.status_code, 200)
                self.assertEqual(options.status_code, 200)

    def test_incremental_sync_and_ordering_parameters_are_bounded(self):
        past = (timezone.now() - timedelta(days=1)).isoformat()
        future = (timezone.now() + timedelta(days=1)).isoformat()
        included = self.client.get('/api/v1/events/', {'updated_since': past})
        excluded = self.client.get('/api/v1/events/', {'updated_since': future})
        invalid = self.client.get('/api/v1/events/', {'ordering': 'created_by'})
        self.assertEqual(included.json()['count'], 1)
        self.assertEqual(excluded.json()['count'], 0)
        self.assertEqual(invalid.status_code, 400)
        self.assertIn('ordering', invalid.json()['errors'])

    def test_related_editorial_changes_advance_the_incremental_sync_cursor(self):
        extra_category = Category.objects.create(name='Música de prueba')

        def assert_synced(change):
            baseline = timezone.now() - timedelta(days=1)
            Event.objects.filter(pk=self.published.pk).update(updated_at=baseline)
            change()
            self.published.refresh_from_db()
            self.assertGreater(self.published.updated_at, baseline + timedelta(hours=12))
            response = self.client.get(
                '/api/v1/events/',
                {'updated_since': (baseline + timedelta(hours=12)).isoformat()},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['count'], 1)
            self.assertEqual(response.json()['results'][0]['id'], str(self.published.pk))

        schedule = self.published.schedule_items.first()
        schedule.title = 'Apertura actualizada'
        assert_synced(schedule.save)
        assert_synced(lambda: self.published.categories.add(extra_category))
        assert_synced(lambda: self.published.categories.remove(extra_category))

        self.category.description = 'Descripción actualizada'
        assert_synced(self.category.save)
        self.audience.name = 'Público actualizado'
        assert_synced(self.audience.save)
        self.place.address = 'Dirección actualizada'
        assert_synced(self.place.save)
        self.organization.description = 'Organización actualizada'
        assert_synced(self.organization.save)

        assert_synced(schedule.delete)

    def test_reverse_category_clear_and_parent_place_edit_advance_cursor(self):
        baseline = timezone.now() - timedelta(days=1)
        Event.objects.filter(pk=self.published.pk).update(updated_at=baseline)
        self.category.events.clear()
        self.published.refresh_from_db()
        self.assertGreater(self.published.updated_at, baseline + timedelta(hours=12))

        parent = Place.objects.create(name='Recinto padre', country_code='MX')
        self.place.parent = parent
        self.place.save()
        Event.objects.filter(pk=self.published.pk).update(updated_at=baseline)
        parent.name = 'Recinto padre actualizado'
        parent.save()
        self.published.refresh_from_db()
        self.assertGreater(self.published.updated_at, baseline + timedelta(hours=12))
