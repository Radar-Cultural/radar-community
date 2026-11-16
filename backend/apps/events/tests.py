from datetime import timedelta

from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Place

from .models import Event, EventPublicationDecision, EventScheduleItem, PublicationAcceptance


class EventModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='editora',
            email='editora@example.test',
            password='not-a-production-password',
        )
        self.place = Place.objects.create(
            name='Recinto de prueba', locality='Puebla', country_code='MX'
        )

    def make_event(self, **overrides):
        values = {
            'title': 'Encuentro cultural de prueba',
            'summary': 'Resumen verificable para pruebas.',
            'description': 'Descripción de prueba.',
            'starts_at': timezone.now() + timedelta(days=2),
            'time_zone': 'America/Mexico_City',
            'place': self.place,
            'external_organizer_name': 'Organización de prueba',
            'source_url': 'https://example.test/fuente',
            'created_by': self.user,
        }
        values.update(overrides)
        return Event(**values)

    def test_end_cannot_precede_start(self):
        event = self.make_event()
        event.ends_at = event.starts_at - timedelta(hours=1)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_online_event_requires_online_url(self):
        event = self.make_event(attendance_mode=Event.ATTENDANCE_ONLINE, place=None)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_publishing_records_timestamp_and_unique_slug(self):
        event = self.make_event(publication_status=Event.PUBLICATION_PUBLISHED)
        event.full_clean()
        event.save()
        second = self.make_event(publication_status=Event.PUBLICATION_PUBLISHED)
        second.full_clean()
        second.save()
        self.assertIsNotNone(event.published_at)
        self.assertNotEqual(event.slug, second.slug)

    def test_expanding_unicode_title_stays_within_slug_limit(self):
        event = self.make_event(title='ﬃ' * 255)
        event.full_clean()
        event.save()
        self.assertLessEqual(len(event.slug), 280)

    def test_schedule_item_validates_dates(self):
        event = self.make_event()
        event.full_clean()
        event.save()
        item = EventScheduleItem(
            event=event,
            title='Actividad',
            starts_at=event.starts_at,
            ends_at=event.starts_at - timedelta(minutes=1),
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_paid_event_normalizes_structured_admission_options(self):
        event = self.make_event(
            admission_type=Event.ADMISSION_PAID,
            admission_options=[{'name': 'General', 'price': 120, 'price_currency': 'mxn'}],
        )
        event.full_clean()
        self.assertEqual(
            event.admission_options,
            [{'name': 'General', 'price': '120', 'price_currency': 'MXN'}],
        )

    def test_paid_event_rejects_invalid_admission_options(self):
        for option in (
            {'name': 'General', 'price': -1, 'price_currency': 'MXN'},
            {'name': 'General', 'price': 100},
            {'name': 'General', 'price': 'NaN', 'price_currency': 'EUR'},
            {'name': 'General', 'price': 'Infinity', 'price_currency': 'EUR'},
            {'name': 'General', 'price': 100, 'price_currency': '元元元'},
        ):
            with self.subTest(option=option):
                event = self.make_event(
                    admission_type=Event.ADMISSION_PAID,
                    admission_options=[option],
                )
                with self.assertRaises(ValidationError):
                    event.full_clean()

    def test_links_require_a_label_and_valid_url(self):
        event = self.make_event(links=[{'label': 'Registro', 'url': 'no-es-url'}])
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_open_data_image_requires_reusable_license_and_attribution(self):
        event = self.make_event(
            image_url='https://example.test/imagen.jpg',
            image_license=Event.IMAGE_ALL_RIGHTS,
            image_credit='Crédito de prueba',
            image_source_url='https://example.test/fuente-imagen',
            include_image_in_open_data=True,
        )
        with self.assertRaises(ValidationError):
            event.full_clean()

        event.image_license = Event.IMAGE_CC_BY
        event.full_clean()

    def test_language_code_accepts_international_tags_and_rejects_invalid_values(self):
        event = self.make_event(language_code='zh-Hant-TW')
        event.full_clean()
        event.language_code = 'not a language tag'
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_publication_requires_a_verified_iana_time_zone(self):
        event = self.make_event(publication_status=Event.PUBLICATION_PUBLISHED, time_zone='')
        with self.assertRaisesMessage(ValidationError, 'zona horaria verificada'):
            event.full_clean()
        event.time_zone = 'Europe/Paris'
        event.full_clean()
        event.time_zone = '../etc/passwd'
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_schedule_item_must_stay_inside_event_dates(self):
        event = self.make_event(ends_at=timezone.now() + timedelta(days=3))
        event.full_clean()
        event.save()
        item = EventScheduleItem(
            event=event,
            title='Actividad fuera de rango',
            starts_at=event.starts_at - timedelta(minutes=1),
        )
        with self.assertRaises(ValidationError):
            item.full_clean()


class EventAdminSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='editora',
            email='editora@example.test',
            password='not-a-production-password',
        )
        self.place = Place.objects.create(
            name='Recinto de prueba', locality='Puebla', country_code='MX'
        )
        self.editor = User.objects.create_user(
            username='otra-editora',
            email='otra-editora@example.test',
            password='not-a-production-password',
            is_staff=True,
        )
        self.publisher = User.objects.create_superuser(
            username='publicadora',
            email='publicadora@example.test',
            password='not-a-production-password',
        )
        self.event_admin = admin.site._registry[Event]
        self.request = RequestFactory().post('/admin/events/event/')

    def make_event(self, **overrides):
        values = {
            'title': 'Encuentro cultural de prueba',
            'summary': 'Resumen verificable para pruebas.',
            'description': 'Descripción de prueba.',
            'starts_at': timezone.now() + timedelta(days=2),
            'time_zone': 'America/Mexico_City',
            'place': self.place,
            'external_organizer_name': 'Organización de prueba',
            'source_url': 'https://example.test/fuente',
            'created_by': self.user,
        }
        values.update(overrides)
        return Event(**values)

    def test_admin_sets_creator_and_publisher_from_authenticated_actor(self):
        self.request.user = self.publisher
        event = self.make_event(created_by=self.editor)
        self.event_admin.save_model(self.request, event, None, change=False)
        self.assertEqual(event.created_by, self.publisher)

        self.request.user = self.editor
        event.publication_status = Event.PUBLICATION_REVIEW
        self.event_admin.save_model(self.request, event, None, change=True)
        self.request.user = self.publisher
        event.publication_status = Event.PUBLICATION_PUBLISHED
        self.event_admin.save_model(self.request, event, None, change=True)
        self.assertEqual(event.published_by, self.publisher)
        self.assertIsNotNone(event.published_at)
        self.assertEqual(self.client.get(f'/api/v1/events/{event.slug}/').status_code, 200)
        self.assertEqual(self.client.get(f'/eventos/{event.slug}/').status_code, 200)
        self.client.force_login(self.publisher)
        change_page = self.client.get(reverse('admin:events_event_change', args=[event.pk]))
        self.assertEqual(change_page.status_code, 200)
        self.assertContains(change_page, 'Event publication decisions')
        self.assertEqual(
            list(
                EventPublicationDecision.objects.filter(event=event)
                .order_by('created_at', 'pk')
                .values_list('previous_status', 'new_status', 'actor_id')
            ),
            [
                (Event.PUBLICATION_DRAFT, Event.PUBLICATION_REVIEW, self.editor.id),
                (Event.PUBLICATION_REVIEW, Event.PUBLICATION_PUBLISHED, self.publisher.id),
            ],
        )

        event.publication_status = Event.PUBLICATION_ARCHIVED
        self.event_admin.save_model(self.request, event, None, change=True)
        self.assertEqual(self.client.get(f'/api/v1/events/{event.slug}/').status_code, 404)
        self.assertEqual(self.client.get(f'/eventos/{event.slug}/').status_code, 404)
        self.assertTrue(
            EventPublicationDecision.objects.filter(
                event=event,
                previous_status=Event.PUBLICATION_PUBLISHED,
                new_status=Event.PUBLICATION_ARCHIVED,
                actor=self.publisher,
            ).exists()
        )

    def test_admin_requires_review_and_rejects_skipping_or_unauthorized_transitions(self):
        self.request.user = self.publisher
        event = self.make_event()
        event.publication_status = Event.PUBLICATION_PUBLISHED
        with self.assertRaises(PermissionDenied):
            self.event_admin.save_model(self.request, event, None, change=False)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

        event.publication_status = Event.PUBLICATION_DRAFT
        self.event_admin.save_model(self.request, event, None, change=False)
        event.publication_status = Event.PUBLICATION_PUBLISHED
        with self.assertRaises(PermissionDenied):
            self.event_admin.save_model(self.request, event, None, change=True)
        event.refresh_from_db()
        self.assertEqual(event.publication_status, Event.PUBLICATION_DRAFT)

        self.request.user = self.editor
        event.publication_status = Event.PUBLICATION_REVIEW
        self.event_admin.save_model(self.request, event, None, change=True)
        event.publication_status = Event.PUBLICATION_DRAFT
        with self.assertRaises(PermissionDenied):
            self.event_admin.save_model(self.request, event, None, change=True)
        event.refresh_from_db()
        self.assertEqual(event.publication_status, Event.PUBLICATION_REVIEW)
        self.assertEqual(EventPublicationDecision.objects.filter(event=event).count(), 1)

    def test_admin_preserves_attribution_and_moderated_visibility(self):
        self.request.user = self.publisher
        event = self.make_event(publication_status=Event.PUBLICATION_PUBLISHED)
        event.save()
        event.visibility_status = Event.VISIBILITY_REMOVED
        event.save(update_fields=['visibility_status'])
        event.created_by = self.publisher
        event.published_by = self.editor
        event.visibility_status = Event.VISIBILITY_PUBLIC
        self.event_admin.save_model(self.request, event, None, change=True)
        event.refresh_from_db()
        self.assertEqual(event.created_by, self.user)
        self.assertIsNone(event.published_by)
        self.assertEqual(event.visibility_status, Event.VISIBILITY_REMOVED)

    def test_non_publisher_cannot_unpublish_or_edit_published_event(self):
        self.request.user = self.editor
        event = self.make_event(publication_status=Event.PUBLICATION_PUBLISHED)
        event.save()
        event.publication_status = Event.PUBLICATION_DRAFT
        with self.assertRaises(PermissionDenied):
            self.event_admin.save_model(self.request, event, None, change=True)
        event.refresh_from_db()
        self.assertEqual(event.publication_status, Event.PUBLICATION_PUBLISHED)
        event.title = 'Intento de edición sin permiso'
        with self.assertRaises(PermissionDenied):
            self.event_admin.save_model(self.request, event, None, change=True)
        event.refresh_from_db()
        self.assertEqual(event.title, 'Encuentro cultural de prueba')
        self.assertFalse(self.event_admin.has_change_permission(self.request, event))

    def test_publication_history_and_acceptances_are_immutable_in_admin(self):
        self.request.user = self.publisher
        self.assertFalse(self.event_admin.has_delete_permission(self.request))
        for model in (EventPublicationDecision, PublicationAcceptance):
            model_admin = admin.site._registry[model]
            self.assertFalse(model_admin.has_add_permission(self.request))
            self.assertFalse(model_admin.has_change_permission(self.request))
            self.assertFalse(model_admin.has_delete_permission(self.request))

    def test_admin_only_offers_permitted_publication_states(self):
        self.request.user = self.editor
        new_choices = dict(
            self.event_admin.get_form(self.request).base_fields['publication_status'].choices
        )
        self.assertEqual(set(new_choices), {Event.PUBLICATION_DRAFT})

        event = self.make_event()
        event.save()
        event.publication_status = Event.PUBLICATION_REVIEW
        event.save(update_fields=['publication_status', 'updated_at'])
        reviewer_choices = dict(
            self.event_admin.get_form(self.request, event).base_fields['publication_status'].choices
        )
        self.assertEqual(set(reviewer_choices), {Event.PUBLICATION_REVIEW})

        self.request.user = self.publisher
        publisher_choices = dict(
            self.event_admin.get_form(self.request, event).base_fields['publication_status'].choices
        )
        self.assertEqual(
            set(publisher_choices),
            {Event.PUBLICATION_REVIEW, Event.PUBLICATION_DRAFT, Event.PUBLICATION_PUBLISHED},
        )
