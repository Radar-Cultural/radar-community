from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.core.exceptions import ValidationError


def validate_iana_time_zone(value):
    try:
        ZoneInfo(value)
    except (ValueError, ZoneInfoNotFoundError) as error:
        raise ValidationError(
            'Usa una zona horaria IANA válida, como America/Mexico_City o Europe/Paris.',
            code='invalid_time_zone',
        ) from error
