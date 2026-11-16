"""Create clearly labelled, local-only events for the Vue and API walkthrough."""

from datetime import timedelta
from urllib.parse import urlsplit

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Category, Place
from apps.events.models import Event, EventScheduleItem

DEMO_EVENTS = (
    (
        'demo-danza',
        'DEMO · Danza en movimiento',
        'Danza',
        'fragment-dance.webp',
        2,
        'America/Mexico_City',
        False,
    ),
    (
        'demo-taller',
        'DEMO · Taller de creación',
        'Taller',
        'community-workshop.webp',
        3,
        'Europe/Paris',
        True,
    ),
    (
        'demo-musica',
        'DEMO · Música en directo',
        'Música',
        'fragment-music.webp',
        4,
        'Asia/Tokyo',
        False,
    ),
)
DEMO_SOURCE = 'https://example.test/radar-cultural/'


class Command(BaseCommand):
    help = 'Crea tres eventos ficticios, sólo en una base SQLite local con DEBUG=True.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--frontend-origin',
            default=settings.FRONTEND_ORIGIN,
            help='Origen local de Vite que sirve las ilustraciones del demo.',
        )

    def handle(self, *args, **options):
        if (
            not settings.DEBUG
            or settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3'
        ):
            raise CommandError('El demo sólo se permite con DEBUG=True y una base SQLite local.')

        origin = options['frontend_origin'].rstrip('/')
        parsed = urlsplit(origin)
        if (
            parsed.scheme != 'http'
            or parsed.hostname not in {'localhost', '127.0.0.1', '::1'}
            or not parsed.port
            or parsed.path
            or parsed.query
            or parsed.fragment
            or parsed.username
            or parsed.password
        ):
            raise CommandError('--frontend-origin debe ser un origen HTTP local con puerto.')

        now = timezone.now()
        with transaction.atomic():
            editor, created = User.objects.get_or_create(
                username='radar-demo-editor',
                defaults={
                    'email': 'radar-demo@example.test',
                    'is_active': False,
                },
            )
            if created:
                editor.set_unusable_password()
                editor.save(update_fields=['password'])
            elif (
                editor.email != 'radar-demo@example.test'
                or editor.is_active
                or editor.has_usable_password()
            ):
                raise CommandError('El usuario reservado para el demo ya pertenece a otra cuenta.')

            paris_place, _ = Place.objects.get_or_create(
                slug='demo-sala-paris',
                defaults={
                    'name': 'DEMO · Sala de creación',
                    'locality': 'Paris',
                    'country_code': 'FR',
                },
            )

            for slug, title, category_name, image_name, day_offset, zone, paid_mixed in DEMO_EVENTS:
                source = f'{DEMO_SOURCE}{slug}'
                existing = Event.objects.filter(slug=slug).first()
                if existing and existing.source_url != source:
                    raise CommandError(f'El slug {slug} ya pertenece a otro evento.')
                category, _ = Category.objects.get_or_create(
                    slug=slug,
                    defaults={'name': f'DEMO · {category_name}'},
                )
                starts_at = now + timedelta(days=day_offset)
                event = existing or Event(slug=slug, created_by=editor)
                event.title = title
                event.summary = 'Evento ficticio para comprobar la integración local.'
                event.description = (
                    'Este evento es una muestra técnica de Radar Cultural. No corresponde a una '
                    'actividad real ni admite inscripciones. La imagen es editorial e ilustrativa.'
                )
                event.language_code = 'es-MX'
                event.time_zone = zone
                event.starts_at = starts_at
                event.ends_at = starts_at + timedelta(hours=3 if paid_mixed else 2)
                event.event_status = Event.STATUS_SCHEDULED
                event.attendance_mode = (
                    Event.ATTENDANCE_MIXED if paid_mixed else Event.ATTENDANCE_ONLINE
                )
                event.place = paris_place if paid_mixed else None
                event.online_url = source
                event.external_organizer_name = 'Radar Cultural · demo local'
                event.source_url = source
                event.admission_type = Event.ADMISSION_PAID if paid_mixed else Event.ADMISSION_FREE
                event.admission_options = (
                    [
                        {
                            'name': 'Acceso de prueba',
                            'price': '12.50',
                            'price_currency': 'EUR',
                            'url': f'{source}/entradas',
                        }
                    ]
                    if paid_mixed
                    else []
                )
                event.links = (
                    [{'label': 'Programa de prueba', 'url': f'{source}/programa'}]
                    if paid_mixed
                    else []
                )
                event.image_url = f'{origin}/src/assets/{image_name}'
                event.image_source_url = event.image_url
                event.image_credit = 'Ilustración editorial de Radar Cultural (demo local)'
                event.image_license = Event.IMAGE_CC0
                event.include_image_in_open_data = True
                event.publication_status = Event.PUBLICATION_PUBLISHED
                event.visibility_status = Event.VISIBILITY_PUBLIC
                event.published_by = editor
                event.full_clean()
                event.save()
                event.categories.set((category,))
                if paid_mixed:
                    EventScheduleItem.objects.update_or_create(
                        event=event,
                        position=0,
                        defaults={
                            'title': 'DEMO · Sesión guiada',
                            'starts_at': starts_at + timedelta(hours=1),
                            'ends_at': starts_at + timedelta(hours=2),
                        },
                    )

        self.stdout.write(self.style.SUCCESS('3 eventos DEMO listos para la agenda local.'))
