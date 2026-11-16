import json
from datetime import UTC
from zoneinfo import ZoneInfo

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from apps.events.models import Event
from apps.events.services.public_fields import public_admission_options, public_links
from apps.events.services.semantic import build_event_schema


def public_event_page(request, slug):
    event = get_object_or_404(
        Event.objects.public()
        .select_related('place', 'place__parent', 'organizer')
        .prefetch_related('categories', 'audiences', 'schedule_items'),
        slug=slug,
    )
    canonical_url = request.build_absolute_uri(reverse('public-event-page', kwargs={'slug': slug}))
    schema = build_event_schema(event, request)
    # JSON inside an HTML script must not contain literal tag delimiters.
    schema_json = json.dumps(schema, ensure_ascii=False).translate(
        {ord('<'): r'\u003C', ord('>'): r'\u003E', ord('&'): r'\u0026'}
    )
    image = schema.get('image')
    event_zone = ZoneInfo(event.time_zone) if event.time_zone else UTC
    with timezone.override(event_zone):
        response = render(
            request,
            'events/detail.html',
            {
                'event': event,
                'canonical_url': canonical_url,
                'schema_json': mark_safe(schema_json),
                'image': image,
                'admission_options': public_admission_options(event.admission_options),
                'event_links': public_links(event.links),
                'organizer_name': (
                    event.organizer.official_name
                    if event.organizer_id
                    else event.external_organizer_name
                ),
            },
        )
    return response
