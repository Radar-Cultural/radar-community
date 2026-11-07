import uuid

from django.conf import settings
from django.db import models

from apps.events.models import Event


class ContentReport(models.Model):
    REASON_INCORRECT = 'incorrect'
    REASON_OUTDATED = 'outdated'
    REASON_RIGHTS = 'rights'
    REASON_PRIVACY = 'privacy'
    REASON_SPAM = 'spam'
    REASON_UNSAFE = 'unsafe'
    REASON_OTHER = 'other'
    REASON_CHOICES = [
        (REASON_INCORRECT, 'Información incorrecta'),
        (REASON_OUTDATED, 'Información desactualizada'),
        (REASON_RIGHTS, 'Derechos o atribución'),
        (REASON_PRIVACY, 'Privacidad o datos personales'),
        (REASON_SPAM, 'Spam o contenido engañoso'),
        (REASON_UNSAFE, 'Riesgo para la comunidad'),
        (REASON_OTHER, 'Otro motivo'),
    ]

    STATUS_SUBMITTED = 'submitted'
    STATUS_IN_REVIEW = 'in_review'
    STATUS_RESOLVED = 'resolved'
    STATUS_DISMISSED = 'dismissed'
    STATUS_CHOICES = [
        (STATUS_SUBMITTED, 'Recibido'),
        (STATUS_IN_REVIEW, 'En revisión'),
        (STATUS_RESOLVED, 'Resuelto'),
        (STATUS_DISMISSED, 'Descartado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='content_reports',
    )
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='reports')
    reported_url = models.URLField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, db_index=True)
    details = models.TextField(max_length=5000)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=STATUS_SUBMITTED, db_index=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_content_reports',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('status', '-created_at')
        permissions = [('review_content_reports', 'Puede revisar reportes de contenido')]

    def __str__(self):
        return f'Reporte {self.id} · {self.get_reason_display()}'


class ModerationDecision(models.Model):
    ACTION_REQUEST_CHANGES = 'request_changes'
    ACTION_HIDE = 'hide'
    ACTION_REMOVE = 'remove'
    ACTION_RESTORE = 'restore'
    ACTION_CHOICES = [
        (ACTION_REQUEST_CHANGES, 'Solicitar correcciones'),
        (ACTION_HIDE, 'Ocultar de la agenda'),
        (ACTION_REMOVE, 'Retirar globalmente'),
        (ACTION_RESTORE, 'Restaurar visibilidad pública'),
    ]

    report = models.ForeignKey(ContentReport, on_delete=models.CASCADE, related_name='decisions')
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='moderation_decisions',
    )
    previous_status = models.CharField(max_length=16, choices=ContentReport.STATUS_CHOICES)
    new_status = models.CharField(max_length=16, choices=ContentReport.STATUS_CHOICES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField(max_length=5000)
    previous_visibility = models.CharField(max_length=16, choices=Event.VISIBILITY_CHOICES)
    new_visibility = models.CharField(max_length=16, choices=Event.VISIBILITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at', '-pk')

    def __str__(self):
        return f'Decisión sobre {self.report_id}'
