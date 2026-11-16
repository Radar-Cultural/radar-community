from datetime import UTC


def _escape(value):
    normalized = str(value or '').replace('\r\n', '\n').replace('\r', '\n')
    normalized = ''.join(
        ' ' if ord(char) < 32 and char not in {'\n', '\t'} else char
        for char in normalized
        if ord(char) != 127
    )
    return (
        normalized.replace('\\', '\\\\')
        .replace('\n', '\\n')
        .replace(',', '\\,')
        .replace(';', '\\;')
    )


def _fold(line):
    physical_lines = []
    current = ''
    byte_length = 0
    for char in line:
        char_length = len(char.encode('utf-8'))
        if byte_length + char_length > 75:
            physical_lines.append(current)
            current = ' ' + char
            byte_length = 1 + char_length
        else:
            current += char
            byte_length += char_length
    physical_lines.append(current)
    return '\r\n'.join(physical_lines)


def _ical_datetime(value):
    return value.astimezone(UTC).strftime('%Y%m%dT%H%M%SZ')


def _calendar_location(event):
    if not event.place_id:
        return event.online_url
    place = event.place
    parts = []
    for part in (
        place.name,
        event.location_details,
        place.address,
        place.locality,
        place.region,
        place.country_code,
    ):
        if part and (not parts or part.casefold() != parts[-1].casefold()):
            parts.append(part)
    return ', '.join(parts)


def render_event_calendar(event, event_url):
    status = 'CANCELLED' if event.event_status == event.STATUS_CANCELLED else 'CONFIRMED'
    location = _calendar_location(event)
    description = f'{event.summary}\nFuente: {event.source_url}'
    if event.place_id and event.online_url:
        description += f'\nAcceso en línea: {event.online_url}'
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Radar Cultural//Radar Cultural API//ES',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'BEGIN:VEVENT',
        f'UID:{event.id}@radarcultural.mx',
        f'DTSTAMP:{_ical_datetime(event.updated_at)}',
        f'DTSTART:{_ical_datetime(event.starts_at)}',
        f'SUMMARY:{_escape(event.title)}',
        f'DESCRIPTION:{_escape(description)}',
        f'LOCATION:{_escape(location)}',
        f'URL:{_escape(event_url)}',
        f'STATUS:{status}',
    ]
    if event.ends_at:
        lines.append(f'DTEND:{_ical_datetime(event.ends_at)}')
    lines.extend(('END:VEVENT', 'END:VCALENDAR', ''))
    return '\r\n'.join(_fold(line) for line in lines)
