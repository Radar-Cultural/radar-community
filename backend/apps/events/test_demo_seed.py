from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.events.models import Event


class DemoSeedTests(TestCase):
    @override_settings(DEBUG=True, FRONTEND_ORIGIN='http://127.0.0.1:5174')
    def test_seed_is_idempotent_and_visible_through_the_public_api(self):
        if connection.vendor != 'sqlite':
            self.skipTest('El comando DEMO se limita deliberadamente a SQLite local.')
        for _ in range(2):
            call_command('seed_demo_events', stdout=StringIO())

        self.assertEqual(Event.objects.count(), 3)
        response = APIClient().get('/api/v1/events/', {'has_image': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)
        for event in response.json()['results']:
            self.assertTrue(event['title'].startswith('DEMO · '))
            self.assertTrue(event['image']['url'].startswith('http://127.0.0.1:5174/'))

    @override_settings(DEBUG=False)
    def test_seed_refuses_production_settings(self):
        with self.assertRaisesMessage(CommandError, 'sólo se permite'):
            call_command('seed_demo_events', stdout=StringIO())
        self.assertFalse(Event.objects.exists())

    @override_settings(DEBUG=True)
    def test_seed_rejects_non_local_asset_origin(self):
        if connection.vendor != 'sqlite':
            self.skipTest('La validación del origen sólo se alcanza en SQLite local.')
        with self.assertRaisesMessage(CommandError, 'origen HTTP local'):
            call_command(
                'seed_demo_events', frontend_origin='https://radarcultural.mx', stdout=StringIO()
            )
        self.assertFalse(Event.objects.exists())
