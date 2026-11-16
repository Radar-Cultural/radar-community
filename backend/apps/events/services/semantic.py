from datetime import UTC
from zoneinfo import ZoneInfo

from django.urls import reverse

from apps.events.models import Event
from apps.events.services.public_fields import public_admission_options, public_links

LICENSE_URLS = {
    Event.DESCRIPTION_CC0: 'https://creativecommons.org/publicdomain/zero/1.0/',
    Event.DESCRIPTION_PERMISSION: None,
    Event.IMAGE_CC0: 'https://creativecommons.org/publicdomain/zero/1.0/',
    Event.IMAGE_CC_BY: 'https://creativecommons.org/licenses/by/4.0/',
    Event.IMAGE_CC_BY_SA: 'https://creativecommons.org/licenses/by-sa/4.0/',
}


def license_url(value):
    return LICENSE_URLS[value]


def _absolute(request, route_name, **kwargs):
    return request.build_absolute_uri(reverse(route_name, kwargs=kwargs))


def _place_schema(place, location_details):
    data = {
        '@type': 'Place',
        '@id': f'urn:uuid:{place.id}',
        'name': place.name,
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': place.address,
            'addressLocality': place.locality,
            'addressRegion': place.region,
            'postalCode': place.postal_code,
            'addressCountry': place.country_code,
        },
    }
    if location_details:
        data['description'] = location_details
    if place.authority_url:
        data['sameAs'] = place.authority_url
    if place.latitude is not None and place.longitude is not None:
        data['geo'] = {
            '@type': 'GeoCoordinates',
            'latitude': str(place.latitude),
            'longitude': str(place.longitude),
        }
    if place.parent_id:
        data['containedInPlace'] = {
            '@type': 'Place',
            '@id': f'urn:uuid:{place.parent_id}',
            'name': place.parent.name,
        }
    return data


def _organizer_schema(event, request):
    if not event.organizer_id:
        return {
            '@type': 'Organization',
            'name': event.external_organizer_name,
            'url': event.source_url,
        }
    organizer = event.organizer
    if not organizer.is_verified:
        return {
            '@type': 'Organization',
            '@id': f'urn:uuid:{organizer.id}',
            'name': organizer.official_name,
            'url': event.source_url,
        }
    data = {
        '@type': 'Organization',
        '@id': f'urn:uuid:{organizer.id}',
        'name': organizer.official_name,
        'url': _absolute(request, 'organization-detail', slug=organizer.slug),
    }
    if organizer.authority_urls:
        data['sameAs'] = organizer.authority_urls
    return data


def _offers(event, event_url):
    if event.admission_type == Event.ADMISSION_FREE:
        return [
            {
                '@type': 'Offer',
                'name': 'Entrada gratuita',
                'price': '0',
                'url': event_url,
                'validFrom': event.published_at.isoformat(),
            }
        ]
    return [
        {
            '@type': 'Offer',
            'name': option['name'],
            'price': option['price'],
            'priceCurrency': option['price_currency'],
            'url': option.get('url', event_url),
            'validFrom': event.published_at.isoformat(),
        }
        for option in public_admission_options(event.admission_options)
    ]


def build_event_schema(event, request):
    event_url = _absolute(request, 'public-event-page', slug=event.slug)
    event_zone = ZoneInfo(event.time_zone) if event.time_zone else UTC
    data = {
        '@context': 'https://schema.org',
        '@type': 'Event',
        '@id': f'urn:uuid:{event.id}',
        'url': event_url,
        'name': event.title,
        'description': event.description,
        'abstract': event.summary,
        'startDate': event.starts_at.astimezone(event_zone).isoformat(),
        'eventStatus': f'https://schema.org/{event.event_status}',
        'eventAttendanceMode': f'https://schema.org/{event.attendance_mode}',
        'organizer': _organizer_schema(event, request),
        'isAccessibleForFree': event.admission_type == Event.ADMISSION_FREE,
        'offers': _offers(event, event_url),
        'subjectOf': event.source_url,
    }
    if description_license := license_url(event.description_license):
        data['license'] = description_license
    if event.ends_at:
        data['endDate'] = event.ends_at.astimezone(event_zone).isoformat()
    if event.language_code:
        data['inLanguage'] = event.language_code
    locations = []
    if event.place_id:
        locations.append(_place_schema(event.place, event.location_details))
    if event.online_url:
        locations.append({'@type': 'VirtualLocation', 'url': event.online_url})
    if locations:
        data['location'] = locations[0] if len(locations) == 1 else locations
    audiences = []
    for audience in event.audiences.all():
        item = {'@type': 'Audience', 'name': audience.name}
        if audience.wikidata_id:
            item['sameAs'] = f'https://www.wikidata.org/wiki/{audience.wikidata_id}'
        audiences.append(item)
    if audiences:
        data['audience'] = audiences
    categories = list(event.categories.all())
    if categories:
        data['keywords'] = [category.name for category in categories]
    schedule_items = list(event.schedule_items.all())
    if schedule_items:
        data['subEvent'] = [
            {
                '@type': 'Event',
                '@id': f'{event_url}#schedule-{item.pk}',
                'name': item.title,
                'startDate': item.starts_at.astimezone(event_zone).isoformat(),
                **(
                    {'endDate': item.ends_at.astimezone(event_zone).isoformat()}
                    if item.ends_at
                    else {}
                ),
                'eventStatus': f'https://schema.org/{event.event_status}',
                'eventAttendanceMode': f'https://schema.org/{event.attendance_mode}',
                'url': event_url,
            }
            for item in schedule_items
        ]
    if links := public_links(event.links):
        data['sameAs'] = [link['url'] for link in links]
    reusable_image_licenses = {Event.IMAGE_CC0, Event.IMAGE_CC_BY, Event.IMAGE_CC_BY_SA}
    if (
        event.include_image_in_open_data
        and event.image_url
        and event.image_license in reusable_image_licenses
    ):
        data['image'] = {
            '@type': 'ImageObject',
            'contentUrl': event.image_url,
            'license': license_url(event.image_license),
            'creditText': event.image_credit,
            'acquireLicensePage': event.image_source_url,
        }
    return data
