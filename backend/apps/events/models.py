import uuid
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator
from django.db import models
from django.utils import timezone

from apps.accounts.models import OrganizationProfile
from apps.catalog.models import Audience, Category, Place
from apps.events.validators import validate_iana_time_zone
from radar_api.identifiers import unique_slug


class EventQuerySet(models.QuerySet):
    def public(self):
        return self.filter(
            publication_status=Event.PUBLICATION_PUBLISHED,
            visibility_status=Event.VISIBILITY_PUBLIC,
            published_at__isnull=False,
        )


class Event(models.Model):
    STATUS_SCHEDULED = 'EventScheduled'
    STATUS_CANCELLED = 'EventCancelled'
    STATUS_POSTPONED = 'EventPostponed'
    STATUS_RESCHEDULED = 'EventRescheduled'
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, 'Programado'),
        (STATUS_CANCELLED, 'Cancelado'),
        (STATUS_POSTPONED, 'Pospuesto'),
        (STATUS_RESCHEDULED, 'Reprogramado'),
    ]

    ATTENDANCE_OFFLINE = 'OfflineEventAttendanceMode'
    ATTENDANCE_ONLINE = 'OnlineEventAttendanceMode'
    ATTENDANCE_MIXED = 'MixedEventAttendanceMode'
    ATTENDANCE_CHOICES = [
        (ATTENDANCE_OFFLINE, 'Presencial'),
        (ATTENDANCE_ONLINE, 'En línea'),
        (ATTENDANCE_MIXED, 'Híbrido'),
    ]

    PUBLICATION_DRAFT = 'draft'
    PUBLICATION_REVIEW = 'in_review'
    PUBLICATION_PUBLISHED = 'published'
    PUBLICATION_ARCHIVED = 'archived'
    PUBLICATION_CHOICES = [
        (PUBLICATION_DRAFT, 'Borrador'),
        (PUBLICATION_REVIEW, 'En revisión'),
        (PUBLICATION_PUBLISHED, 'Publicado'),
        (PUBLICATION_ARCHIVED, 'Archivado'),
    ]

    VISIBILITY_PUBLIC = 'public'
    VISIBILITY_HIDDEN = 'hidden'
    VISIBILITY_REMOVED = 'removed'
    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, 'Visible públicamente'),
        (VISIBILITY_HIDDEN, 'Oculto de la agenda'),
        (VISIBILITY_REMOVED, 'Retirado por moderación'),
    ]

    ADMISSION_FREE = 'free'
    ADMISSION_PAID = 'paid'
    ADMISSION_CHOICES = [
        (ADMISSION_FREE, 'Entrada gratuita'),
        (ADMISSION_PAID, 'Entrada con costo'),
    ]

    CONTRIBUTION_ORGANIZER = 'organizer'
    CONTRIBUTION_PUBLIC_SOURCE = 'public_source'
    CONTRIBUTION_CHOICES = [
        (CONTRIBUTION_ORGANIZER, 'Organiza el evento'),
        (CONTRIBUTION_PUBLIC_SOURCE, 'Aporta información pública'),
    ]

    DESCRIPTION_CC0 = 'CC0-1.0'
    DESCRIPTION_PERMISSION = 'permission-recorded'
    DESCRIPTION_LICENSE_CHOICES = [
        (DESCRIPTION_CC0, 'CC0 1.0 Universal'),
        (DESCRIPTION_PERMISSION, 'Permiso registrado'),
    ]

    IMAGE_CC0 = 'CC0-1.0'
    IMAGE_CC_BY = 'CC-BY-4.0'
    IMAGE_CC_BY_SA = 'CC-BY-SA-4.0'
    IMAGE_ALL_RIGHTS = 'all-rights-reserved'
    IMAGE_LICENSE_CHOICES = [
        (IMAGE_CC0, 'CC0 1.0 Universal'),
        (IMAGE_CC_BY, 'CC BY 4.0'),
        (IMAGE_CC_BY_SA, 'CC BY-SA 4.0'),
        (IMAGE_ALL_RIGHTS, 'Todos los derechos reservados'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=500)
    description = models.TextField(max_length=10_000)
    language_code = models.CharField(
        max_length=35,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$',
                message='Usa una etiqueta de idioma como es-MX, en-US o zh-Hant-TW.',
            )
        ],
        help_text='Idioma principal verificado del contenido; puede quedar vacío.',
    )
    time_zone = models.CharField(
        max_length=64,
        blank=True,
        validators=[validate_iana_time_zone],
        help_text='Zona IANA verificada del horario. Obligatoria para publicar eventos nuevos.',
    )
    starts_at = models.DateTimeField(db_index=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    event_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    attendance_mode = models.CharField(
        max_length=50,
        choices=ATTENDANCE_CHOICES,
        default=ATTENDANCE_OFFLINE,
    )
    publication_status = models.CharField(
        max_length=16,
        choices=PUBLICATION_CHOICES,
        default=PUBLICATION_DRAFT,
        db_index=True,
    )
    visibility_status = models.CharField(
        max_length=16,
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_PUBLIC,
        db_index=True,
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='events',
    )
    location_details = models.CharField(max_length=500, blank=True)
    online_url = models.URLField(blank=True)
    organizer = models.ForeignKey(
        OrganizationProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='events',
    )
    external_organizer_name = models.CharField(max_length=255, blank=True)
    contribution_role = models.CharField(
        max_length=20,
        choices=CONTRIBUTION_CHOICES,
        default=CONTRIBUTION_ORGANIZER,
    )
    source_url = models.URLField(
        help_text='Fuente pública u oficial que permite verificar la información.',
    )
    admission_type = models.CharField(
        max_length=8,
        choices=ADMISSION_CHOICES,
        default=ADMISSION_FREE,
    )
    admission_options = models.JSONField(default=list, blank=True)
    links = models.JSONField(default=list, blank=True)
    image_url = models.URLField(blank=True)
    image_license = models.CharField(
        max_length=32,
        choices=IMAGE_LICENSE_CHOICES,
        default=IMAGE_ALL_RIGHTS,
    )
    image_credit = models.CharField(max_length=255, blank=True)
    image_source_url = models.URLField(blank=True)
    include_image_in_open_data = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='events')
    audiences = models.ManyToManyField(Audience, related_name='events', blank=True)
    description_license = models.CharField(
        max_length=32,
        choices=DESCRIPTION_LICENSE_CHOICES,
        default=DESCRIPTION_CC0,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_events',
    )
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='published_events',
    )
    published_at = models.DateTimeField(null=True, blank=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('starts_at', 'title')
        indexes = [
            models.Index(
                fields=('publication_status', 'visibility_status', 'starts_at'),
                name='event_public_start_idx',
            ),
            models.Index(fields=('event_status', 'starts_at'), name='event_status_start_idx'),
        ]
        permissions = [
            ('review_event', 'Puede revisar eventos'),
            ('publish_event', 'Puede publicar eventos'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(
                Event,
                value=self.title,
                pk=self.pk,
                prefix='evento',
                max_length=self._meta.get_field('slug').max_length,
            )
        if self.publication_status == self.PUBLICATION_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.publication_status == self.PUBLICATION_PUBLISHED and not self.time_zone:
            errors['time_zone'] = 'Indica la zona horaria verificada antes de publicar.'
        if self.ends_at and self.ends_at < self.starts_at:
            errors['ends_at'] = 'La fecha de término no puede ser anterior al inicio.'
        if (
            self.attendance_mode in (self.ATTENDANCE_OFFLINE, self.ATTENDANCE_MIXED)
            and not self.place
        ):
            errors['place'] = 'Los eventos presenciales o híbridos requieren un lugar.'
        if (
            self.attendance_mode in (self.ATTENDANCE_ONLINE, self.ATTENDANCE_MIXED)
            and not self.online_url
        ):
            errors['online_url'] = 'Los eventos en línea o híbridos requieren un enlace.'
        if self.admission_type == self.ADMISSION_FREE and self.admission_options:
            errors['admission_options'] = 'Un evento gratuito no debe declarar opciones de cobro.'
        if self.admission_type == self.ADMISSION_PAID:
            option_errors = self._validate_admission_options()
            if option_errors:
                errors['admission_options'] = option_errors
        link_errors = self._validate_links()
        if link_errors:
            errors['links'] = link_errors
        if not self.organizer and not self.external_organizer_name.strip():
            errors['external_organizer_name'] = (
                'Indica una organización o el nombre público responsable.'
            )
        if self.include_image_in_open_data:
            if not self.image_url:
                errors['image_url'] = 'Indica la URL de la imagen que se publicará.'
            if not self.image_credit.strip():
                errors['image_credit'] = 'El crédito es obligatorio para publicar la imagen.'
            if not self.image_source_url:
                errors['image_source_url'] = 'Indica la fuente original de la imagen.'
            if self.image_license == self.IMAGE_ALL_RIGHTS:
                errors['image_license'] = (
                    'Una imagen con todos los derechos reservados no puede abrirse en la API.'
                )
        if errors:
            raise ValidationError(errors)

    def _validate_admission_options(self):
        if not isinstance(self.admission_options, list) or not self.admission_options:
            return 'Un evento con costo requiere al menos una opción de entrada.'
        validator = URLValidator()
        normalized = []
        for index, option in enumerate(self.admission_options, start=1):
            if not isinstance(option, dict):
                return f'La opción {index} debe ser un objeto.'
            name = str(option.get('name', '')).strip()
            currency = str(option.get('price_currency', '')).strip().upper()
            try:
                price = Decimal(str(option.get('price', '')))
            except (InvalidOperation, TypeError, ValueError):
                return f'La opción {index} requiere un precio numérico.'
            if not name:
                return f'La opción {index} requiere nombre.'
            if not price.is_finite() or price < 0:
                return f'La opción {index} requiere un precio finito y no negativo.'
            if len(currency) != 3 or not currency.isascii() or not currency.isalpha():
                return f'La opción {index} requiere una moneda de tres letras ASCII.'
            purchase_url = str(option.get('url', '')).strip()
            if purchase_url:
                try:
                    validator(purchase_url)
                except ValidationError:
                    return f'La opción {index} contiene una URL de compra inválida.'
            normalized_option = {
                'name': name,
                'price': format(price, 'f'),
                'price_currency': currency,
            }
            if purchase_url:
                normalized_option['url'] = purchase_url
            normalized.append(normalized_option)
        self.admission_options = normalized
        return ''

    def _validate_links(self):
        if not isinstance(self.links, list):
            return 'Los enlaces deben enviarse como una lista.'
        validator = URLValidator()
        normalized = []
        for index, link in enumerate(self.links, start=1):
            if not isinstance(link, dict):
                return f'El enlace {index} debe ser un objeto.'
            label = str(link.get('label', '')).strip()
            url = str(link.get('url', '')).strip()
            if not label or not url:
                return f'El enlace {index} requiere etiqueta y URL.'
            try:
                validator(url)
            except ValidationError:
                return f'El enlace {index} contiene una URL inválida.'
            normalized.append({'label': label, 'url': url})
        self.links = normalized
        return ''

    @property
    def organizer_name(self):
        if self.organizer_id:
            return self.organizer.official_name
        return self.external_organizer_name


class EventScheduleItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedule_items')
    title = models.CharField(max_length=255)
    starts_at = models.DateTimeField(db_index=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('starts_at', 'position', 'pk')
        constraints = [
            models.UniqueConstraint(
                fields=('event', 'position'),
                name='unique_event_schedule_position',
            ),
        ]

    def __str__(self):
        return f'{self.event}: {self.title}'

    def clean(self):
        errors = {}
        if self.ends_at and self.ends_at < self.starts_at:
            errors['ends_at'] = 'El término no puede ser anterior al inicio.'
        if self.event_id and self.starts_at < self.event.starts_at:
            errors['starts_at'] = 'La actividad no puede iniciar antes que el evento.'
        if self.event_id and self.event.ends_at:
            if self.starts_at > self.event.ends_at:
                errors['starts_at'] = 'La actividad no puede iniciar después que el evento.'
            if self.ends_at and self.ends_at > self.event.ends_at:
                errors['ends_at'] = 'La actividad no puede terminar después que el evento.'
        if errors:
            raise ValidationError(errors)


class EventContributor(models.Model):
    ROLE_EDITOR = 'editor'
    ROLE_REVIEWER = 'reviewer'
    ROLE_CHOICES = [
        (ROLE_EDITOR, 'Puede editar'),
        (ROLE_REVIEWER, 'Puede revisar'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='contributors')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_contributions',
    )
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default=ROLE_EDITOR)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='event_invitations_sent',
    )
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('event', 'user'), name='unique_event_contributor'),
        ]

    def __str__(self):
        return f'{self.user} · {self.event} · {self.get_role_display()}'


class PublicationAcceptance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='acceptances')
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='publication_acceptances',
    )
    terms_version = models.CharField(max_length=32)
    conduct_version = models.CharField(max_length=32)
    description_license = models.CharField(max_length=32, choices=Event.DESCRIPTION_LICENSE_CHOICES)
    confirms_accuracy = models.BooleanField(default=False)
    confirms_rights = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-accepted_at',)

    def __str__(self):
        return f'{self.event} · {self.terms_version}'


class EventPublicationDecision(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='publication_decisions',
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='event_publication_decisions',
    )
    previous_status = models.CharField(max_length=16, choices=Event.PUBLICATION_CHOICES)
    new_status = models.CharField(max_length=16, choices=Event.PUBLICATION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created_at', '-pk')

    def __str__(self):
        return f'{self.event} · {self.previous_status} → {self.new_status}'
