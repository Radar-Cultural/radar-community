from datetime import timedelta

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import RequestFactory, TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Place
from apps.events.models import Event

from .models import ContentReport, ModerationDecision
from .services import record_moderation_decision


class ModerationServiceTests(TestCase):
    def setUp(self):
        self.editor = User.objects.create_user(
            username='moderation-editor',
            email='moderation-editor@example.test',
            password='not-a-production-password',
        )
        self.moderator = User.objects.create_user(
            username='moderator',
            email='moderator@example.test',
            password='not-a-production-password',
        )
        permission = Permission.objects.get(codename='review_content_reports')
        self.moderator.user_permissions.add(permission)
        self.place = Place.objects.create(
            name='Lugar moderado', locality='Puebla', country_code='MX'
        )
        self.event = Event.objects.create(
            title='Evento sujeto a moderación',
            summary='Resumen de prueba.',
            description='Descripción de prueba.',
            starts_at=timezone.now() + timedelta(days=2),
            time_zone='America/Mexico_City',
            place=self.place,
            external_organizer_name='Organización de prueba',
            source_url='https://example.test/evento',
            created_by=self.editor,
            publication_status=Event.PUBLICATION_PUBLISHED,
        )
        self.report = ContentReport.objects.create(
            reporter=self.editor,
            event=self.event,
            reported_url=f'https://radarcultural.mx/eventos/{self.event.slug}',
            reason=ContentReport.REASON_INCORRECT,
            details='La fecha necesita revisión.',
        )

    def test_hide_is_atomic_and_audited(self):
        decision = record_moderation_decision(
            report=self.report,
            moderator=self.moderator,
            action=ModerationDecision.ACTION_HIDE,
            reason='La fuente oficial contradice la fecha publicada.',
        )
        self.event.refresh_from_db()
        self.report.refresh_from_db()
        self.assertEqual(self.event.visibility_status, Event.VISIBILITY_HIDDEN)
        self.assertEqual(self.report.status, ContentReport.STATUS_RESOLVED)
        self.assertEqual(decision.previous_visibility, Event.VISIBILITY_PUBLIC)
        self.assertEqual(decision.new_visibility, Event.VISIBILITY_HIDDEN)
        self.assertEqual(decision.moderator, self.moderator)

    def test_request_changes_preserves_visibility(self):
        decision = record_moderation_decision(
            report=self.report,
            moderator=self.moderator,
            action=ModerationDecision.ACTION_REQUEST_CHANGES,
            reason='Se requiere una fuente oficial adicional.',
        )
        self.event.refresh_from_db()
        self.report.refresh_from_db()
        self.assertEqual(self.event.visibility_status, Event.VISIBILITY_PUBLIC)
        self.assertEqual(self.report.status, ContentReport.STATUS_IN_REVIEW)
        self.assertEqual(decision.previous_visibility, decision.new_visibility)

    def test_decision_requires_permission_and_reason(self):
        with self.assertRaises(PermissionDenied):
            record_moderation_decision(
                report=self.report,
                moderator=self.editor,
                action=ModerationDecision.ACTION_HIDE,
                reason='Sin permiso.',
            )
        with self.assertRaises(ValidationError):
            record_moderation_decision(
                report=self.report,
                moderator=self.moderator,
                action=ModerationDecision.ACTION_HIDE,
                reason=' ',
            )

    def test_admin_cannot_overwrite_report_provenance_or_decision_status(self):
        request = RequestFactory().post('/admin/moderation/contentreport/')
        request.user = self.moderator
        report_admin = admin.site._registry[ContentReport]
        self.report.reporter = self.moderator
        self.report.status = ContentReport.STATUS_RESOLVED
        self.report.assigned_to = self.moderator
        report_admin.save_model(request, self.report, None, change=True)
        self.report.refresh_from_db()
        self.assertEqual(self.report.reporter, self.editor)
        self.assertEqual(self.report.status, ContentReport.STATUS_SUBMITTED)
        self.assertIsNone(self.report.assigned_to)
