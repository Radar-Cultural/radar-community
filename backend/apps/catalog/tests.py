from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Audience, Category, Place, PlaceAlias, normalize_catalog_text


class PlaceIdentityTests(TestCase):
    def test_normalization_preserves_non_latin_names_and_latin_accent_folding(self):
        self.assertEqual(normalize_catalog_text('Café'), 'cafe')
        self.assertEqual(normalize_catalog_text('北京'), '北京')
        self.assertEqual(normalize_catalog_text('नाटक'), 'नाटक')
        self.assertEqual(normalize_catalog_text('مسرح'), 'مسرح')

    def test_same_venue_name_can_exist_in_different_regions_and_countries(self):
        mexico = Place.objects.create(
            name='Centro cultural',
            address='Calle Mayor 1',
            locality='Puebla',
            region='Puebla',
            country_code='MX',
        )
        spain = Place.objects.create(
            name='Centro cultural',
            address='Calle Mayor 1',
            locality='Puebla',
            region='Aragón',
            country_code='ES',
        )
        other_region = Place.objects.create(
            name='Centro cultural',
            address='Calle Mayor 1',
            locality='Puebla',
            region='Otra región',
            country_code='MX',
        )

        self.assertEqual(len({mexico.slug, spain.slug, other_region.slug}), 3)
        self.assertEqual(
            len({mexico.identity_key, spain.identity_key, other_region.identity_key}), 3
        )

    def test_country_is_explicit_and_normalized(self):
        missing = Place(name='Centro cultural')
        with self.assertRaises(ValidationError):
            missing.full_clean()

        place = Place(name='Centro cultural', country_code='fr')
        place.full_clean()
        place.save()
        self.assertEqual(place.country_code, 'FR')

    def test_alias_can_be_shared_by_places_but_not_duplicated_within_one_place(self):
        mexico = Place.objects.create(name='Casa de arte', country_code='MX')
        spain = Place.objects.create(name='Casa de arte', country_code='ES')
        PlaceAlias.objects.create(place=mexico, name='La Casa')
        PlaceAlias.objects.create(place=spain, name='La Casa')

        response = self.client.get('/api/v1/places/', {'q': 'La Casa'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

        with self.assertRaises(IntegrityError), transaction.atomic():
            PlaceAlias.objects.create(place=mexico, name='la casa')

    def test_non_latin_place_names_and_aliases_keep_distinct_identities(self):
        beijing = Place.objects.create(name='北京', locality='北京', country_code='CN')
        shanghai = Place.objects.create(name='上海', locality='北京', country_code='CN')
        self.assertNotEqual(beijing.identity_key, shanghai.identity_key)
        self.assertTrue(beijing.slug.startswith('lugar-'))
        self.assertTrue(shanghai.slug.startswith('lugar-'))

        first = PlaceAlias.objects.create(place=beijing, name='音乐厅')
        second = PlaceAlias.objects.create(place=beijing, name='美术馆')
        self.assertNotEqual(first.normalized_name, second.normalized_name)

    def test_non_latin_catalog_names_receive_stable_ascii_slugs(self):
        first = Category.objects.create(name='文学')
        second = Category.objects.create(name='音乐')
        third = Audience.objects.create(name='一般')
        self.assertTrue(first.slug.startswith('category-'))
        self.assertTrue(second.slug.startswith('category-'))
        self.assertNotEqual(first.slug, second.slug)
        self.assertTrue(third.slug.startswith('audience-'))
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {item['slug'] for item in response.json()['results']}, {first.slug, second.slug}
        )

    def test_expanding_unicode_names_fit_indexes_and_slug_columns(self):
        long_name = 'ﬃ' * 255
        place = Place.objects.create(name=long_name, country_code='FR')
        alias = PlaceAlias.objects.create(place=place, name=long_name)
        self.assertEqual(len(place.normalized_name), 255)
        self.assertEqual(len(alias.normalized_name), 255)
        self.assertLessEqual(len(place.slug), 280)

        first = Category.objects.create(name='ﬃ' * 160)
        second = Category.objects.create(name='ﬃ' * 159 + 'ﬂ')
        self.assertLessEqual(len(first.slug), 180)
        self.assertLessEqual(len(second.slug), 180)
        self.assertNotEqual(first.slug, second.slug)
