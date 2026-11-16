from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from apps.events.models import Event

from .models import ContentReport, ModerationDecision

ACTION_EFFECTS = {
    ModerationDecision.ACTION_REQUEST_CHANGES: (None, ContentReport.STATUS_IN_REVIEW),
    ModerationDecision.ACTION_HIDE: (Event.VISIBILITY_HIDDEN, ContentReport.STATUS_RESOLVED),
    ModerationDecision.ACTION_REMOVE: (Event.VISIBILITY_REMOVED, ContentReport.STATUS_RESOLVED),
    ModerationDecision.ACTION_RESTORE: (Event.VISIBILITY_PUBLIC, ContentReport.STATUS_RESOLVED),
}


@transaction.atomic
def record_moderation_decision(*, report, moderator, action, reason):
    if not moderator.has_perm('moderation.review_content_reports'):
        raise PermissionDenied('No tienes permiso para revisar reportes de contenido.')
    reason = reason.strip()
    if not reason:
        raise ValidationError({'reason': 'La decisión requiere una justificación.'})
    if action not in ACTION_EFFECTS:
        raise ValidationError({'action': 'Selecciona una acción de moderación válida.'})

    locked_report = ContentReport.objects.select_for_update().get(pk=report.pk)
    if locked_report.event_id is None:
        raise ValidationError(
            {'report': 'El evento ya no existe; conserva el reporte sin cambiar visibilidad.'}
        )

    event = Event.objects.select_for_update().get(pk=locked_report.event_id)
    previous_status = locked_report.status
    previous_visibility = event.visibility_status
    new_visibility, new_status = ACTION_EFFECTS[action]
    if new_visibility is None:
        new_visibility = previous_visibility

    event.visibility_status = new_visibility
    event.save(update_fields=['visibility_status', 'updated_at'])
    locked_report.status = new_status
    locked_report.assigned_to = moderator
    locked_report.save(update_fields=['status', 'assigned_to', 'updated_at'])

    return ModerationDecision.objects.create(
        report=locked_report,
        moderator=moderator,
        previous_status=previous_status,
        new_status=new_status,
        action=action,
        reason=reason,
        previous_visibility=previous_visibility,
        new_visibility=new_visibility,
    )
