from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import User
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
        self.category = Category.objects.create(name='Artes escénicas')
        self.audience = Audience.objects.create(name='Público general')
        self.place = Place.objects.create(name='Foro de prueba', locality='Puebla')
        self.published = self.create_event('Evento publicado', Event.PUBLICATION_PUBLISHED)
        self.draft = self.create_event('Evento privado', Event.PUBLICATION_DRAFT)

    def create_event(self, title, publication_status):
        event = Event(
            title=title,
            summary=f'Resumen de {title}',
            description=f'Descripción de {title}',
            starts_at=timezone.now() + timedelta(days=4),
            place=self.place,
            external_organizer_name='Organización pública',
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

    def test_draft_detail_is_not_discoverable(self):
        response = self.client.get(f'/api/v1/events/{self.draft.slug}/')
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

    def test_invalid_place_returns_structured_error(self):
        response = self.client.get('/api/v1/events/', {'place': 'no-es-uuid'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'La solicitud contiene parámetros inválidos.')
        self.assertIn('place', response.json()['errors'])

    def test_catalogs_are_paginated_and_inactive_rows_are_hidden(self):
        Category.objects.create(name='Oculta', is_active=False)
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
