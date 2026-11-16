from django.contrib import admin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from .models import OrganizationProfile, User


class OrganizationAdminSecurityTests(TestCase):
    def setUp(self):
        self.organization_user = User.objects.create_user(
            username='organizacion-de-prueba',
            email='organizacion@example.test',
            account_type=User.ACCOUNT_ORGANIZATION,
        )
        self.other_user = User.objects.create_user(
            username='otra-organizacion',
            email='otra-organizacion@example.test',
            account_type=User.ACCOUNT_ORGANIZATION,
        )
        self.editor = User.objects.create_user(
            username='editora-organizaciones',
            email='editora@example.test',
            is_staff=True,
        )
        self.editor.user_permissions.add(
            Permission.objects.get(codename='change_organizationprofile')
        )
        self.verifier = User.objects.create_superuser(
            username='verificadora',
            email='verificadora@example.test',
        )
        self.profile = OrganizationProfile.objects.create(
            user=self.organization_user,
            official_name='Organización de prueba',
            contact_email='contacto@example.test',
        )
        self.model_admin = admin.site._registry[OrganizationProfile]
        self.request = RequestFactory().post('/admin/accounts/organizationprofile/')

    def test_general_editor_cannot_verify_or_revoke_organization(self):
        self.request.user = self.editor
        self.assertIn(
            'is_verified', self.model_admin.get_readonly_fields(self.request, self.profile)
        )
        self.profile.is_verified = True
        with self.assertRaises(PermissionDenied):
            self.model_admin.save_model(self.request, self.profile, None, change=True)
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_verified)

        self.request.user = self.verifier
        self.profile.is_verified = True
        self.model_admin.save_model(self.request, self.profile, None, change=True)
        self.request.user = self.editor
        self.profile.is_verified = False
        with self.assertRaises(PermissionDenied):
            self.model_admin.save_model(self.request, self.profile, None, change=True)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_verified)

    def test_verification_actor_and_organization_owner_cannot_be_forged(self):
        self.request.user = self.verifier
        self.profile.is_verified = True
        self.profile.verified_by = self.editor
        self.model_admin.save_model(self.request, self.profile, None, change=True)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.verified_by, self.verifier)
        self.assertIsNotNone(self.profile.verified_at)
        verified_at = self.profile.verified_at

        self.request.user = self.editor
        self.profile.user = self.other_user
        self.profile.verified_by = self.editor
        self.profile.verified_at = None
        self.profile.description = 'Actualización editorial.'
        self.model_admin.save_model(self.request, self.profile, None, change=True)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user, self.organization_user)
        self.assertEqual(self.profile.verified_by, self.verifier)
        self.assertEqual(self.profile.verified_at, verified_at)
        self.assertEqual(self.profile.description, 'Actualización editorial.')

        self.request.user = self.verifier
        self.profile.is_verified = False
        self.model_admin.save_model(self.request, self.profile, None, change=True)
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_verified)
        self.assertIsNone(self.profile.verified_by)
        self.assertIsNone(self.profile.verified_at)


class OrganizationSlugTests(TestCase):
    def test_non_latin_organization_names_have_nonempty_unique_slugs(self):
        first_user = User.objects.create_user(username='first-org', email='first@example.test')
        second_user = User.objects.create_user(username='second-org', email='second@example.test')
        first = OrganizationProfile.objects.create(
            user=first_user,
            official_name='文化中心',
            contact_email='first@example.test',
        )
        second = OrganizationProfile.objects.create(
            user=second_user,
            official_name='艺术中心',
            contact_email='second@example.test',
        )
        self.assertTrue(first.slug.startswith('organizacion-'))
        self.assertTrue(second.slug.startswith('organizacion-'))
        self.assertNotEqual(first.slug, second.slug)
        first.is_verified = True
        first.save(update_fields=['is_verified', 'verified_at'])
        response = self.client.get(f'/api/v1/organizations/{first.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], '文化中心')

    def test_expanding_unicode_name_stays_within_slug_limit(self):
        user = User.objects.create_user(username='long-org', email='long@example.test')
        profile = OrganizationProfile.objects.create(
            user=user,
            official_name='ﬃ' * 255,
            contact_email='long@example.test',
        )
        self.assertLessEqual(len(profile.slug), 280)
