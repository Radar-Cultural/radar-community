from datetime import timedelta

from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Category, Place

from .models import Event, EventPublicationDecision


class AdminPublicationHttpTests(TestCase):
    def setUp(self):
        self.publisher = User.objects.create_superuser(
            username='publicadora-http',
            email='publicadora-http@example.test',
            password='not-a-production-password',
        )
        place = Place.objects.create(name='Sala HTTP', country_code='MX')
        self.category = Category.objects.create(name='Música')
        self.event = Event.objects.create(
            title='Evento del formulario administrativo',
            summary='Resumen para comprobar el recorrido de publicación.',
            description='Contenido del evento de prueba.',
            starts_at=timezone.now() + timedelta(days=2),
            time_zone='America/Mexico_City',
            place=place,
            external_organizer_name='Organización de prueba',
            source_url='https://example.test/actividad',
            created_by=self.publisher,
        )
        self.event.categories.add(self.category)
        self.path = reverse('admin:events_event_change', args=[self.event.pk])
        self.client = Client(enforce_csrf_checks=True)

    def form_data(self, status):
        start = timezone.localtime(self.event.starts_at)
        data = {
            'title': self.event.title,
            'summary': self.event.summary,
            'description': self.event.description,
            'language_code': '',
            'time_zone': self.event.time_zone,
            'starts_at_0': start.date().isoformat(),
            'starts_at_1': start.time().strftime('%H:%M:%S'),
            'ends_at_0': '',
            'ends_at_1': '',
            'event_status': Event.STATUS_SCHEDULED,
            'attendance_mode': Event.ATTENDANCE_OFFLINE,
            'publication_status': status,
            'place': str(self.event.place_id),
            'location_details': '',
            'online_url': '',
            'organizer': '',
            'external_organizer_name': self.event.external_organizer_name,
            'contribution_role': Event.CONTRIBUTION_ORGANIZER,
            'source_url': self.event.source_url,
            'admission_type': Event.ADMISSION_FREE,
            'admission_options': '[]',
            'links': '[]',
            'image_url': '',
            'image_license': Event.IMAGE_ALL_RIGHTS,
            'image_credit': '',
            'image_source_url': '',
            'description_license': Event.DESCRIPTION_CC0,
            'categories': [str(self.category.pk)],
            'schedule_items-TOTAL_FORMS': '0',
            'schedule_items-INITIAL_FORMS': '0',
            'schedule_items-MIN_NUM_FORMS': '0',
            'schedule_items-MAX_NUM_FORMS': '1000',
            'contributors-TOTAL_FORMS': '0',
            'contributors-INITIAL_FORMS': '0',
            'contributors-MIN_NUM_FORMS': '0',
            'contributors-MAX_NUM_FORMS': '1000',
            'publication_decisions-TOTAL_FORMS': '0',
            'publication_decisions-INITIAL_FORMS': '0',
            'publication_decisions-MIN_NUM_FORMS': '0',
            'publication_decisions-MAX_NUM_FORMS': '1000',
        }
        return data

    def test_admin_form_requires_csrf_and_publishes_only_after_review(self):
        self.assertEqual(self.client.get(self.path).status_code, 302)
        self.client.force_login(self.publisher)
        page = self.client.get(self.path)
        self.assertEqual(page.status_code, 200)
        token = self.client.cookies['csrftoken'].value

        denied = self.client.post(self.path, self.form_data(Event.PUBLICATION_REVIEW))
        self.assertEqual(denied.status_code, 403)
        self.event.refresh_from_db()
        self.assertEqual(self.event.publication_status, Event.PUBLICATION_DRAFT)

        skipped_review = self.client.post(
            self.path,
            self.form_data(Event.PUBLICATION_PUBLISHED),
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(skipped_review.status_code, 200)
        self.assertIn('publication_status', skipped_review.context['adminform'].form.errors)
        self.event.refresh_from_db()
        self.assertEqual(self.event.publication_status, Event.PUBLICATION_DRAFT)

        for status in (Event.PUBLICATION_REVIEW, Event.PUBLICATION_PUBLISHED):
            with self.subTest(status=status):
                response = self.client.post(
                    self.path,
                    self.form_data(status),
                    HTTP_X_CSRFTOKEN=token,
                )
                self.assertEqual(
                    response.status_code,
                    302,
                    (
                        response.context['adminform'].form.errors,
                        [
                            (inline.formset.prefix, inline.formset.non_form_errors())
                            for inline in response.context['inline_admin_formsets']
                        ],
                    )
                    if response.context
                    else None,
                )
                self.event.refresh_from_db()
                self.assertEqual(self.event.publication_status, status)

        self.assertEqual(self.client.get(f'/api/v1/events/{self.event.slug}/').status_code, 200)
        self.assertEqual(
            list(
                EventPublicationDecision.objects.filter(event=self.event)
                .order_by('created_at')
                .values_list('previous_status', 'new_status')
            ),
            [
                (Event.PUBLICATION_DRAFT, Event.PUBLICATION_REVIEW),
                (Event.PUBLICATION_REVIEW, Event.PUBLICATION_PUBLISHED),
            ],
        )

    def test_staff_without_publish_permission_cannot_edit_published_event(self):
        self.event.publication_status = Event.PUBLICATION_PUBLISHED
        self.event.save(update_fields=['publication_status', 'published_at', 'updated_at'])
        editor = User.objects.create_user(
            username='editor-http',
            email='editor-http@example.test',
            password='not-a-production-password',
            is_staff=True,
        )
        editor.user_permissions.add(Permission.objects.get(codename='change_event'))
        self.client.force_login(editor)
        self.client.get('/admin/')
        token = self.client.cookies['csrftoken'].value

        self.assertEqual(self.client.get(self.path).status_code, 200)
        response = self.client.post(
            self.path,
            self.form_data(Event.PUBLICATION_DRAFT),
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, 403)
        self.event.refresh_from_db()
        self.assertEqual(self.event.publication_status, Event.PUBLICATION_PUBLISHED)
