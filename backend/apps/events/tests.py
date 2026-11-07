from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Place

from .models import Event, EventScheduleItem


class EventModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='editora',
            email='editora@example.test',
            password='not-a-production-password',
        )
        self.place = Place.objects.create(name='Recinto de prueba', locality='Puebla')

    def make_event(self, **overrides):
        values = {
            'title': 'Encuentro cultural de prueba',
            'summary': 'Resumen verificable para pruebas.',
            'description': 'Descripción de prueba.',
            'starts_at': timezone.now() + timedelta(days=2),
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
