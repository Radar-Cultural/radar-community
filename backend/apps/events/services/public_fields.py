"""Project structured editorial fields onto the documented public shape."""

from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

_validate_url = URLValidator()


def _valid_url(value):
    if not isinstance(value, str) or not value:
        return False
    try:
        _validate_url(value)
    except ValidationError:
        return False
    return True


def public_admission_options(values):
    if not isinstance(values, list):
        return []
    options = []
    for option in values:
        if not isinstance(option, dict):
            continue
        name, price, currency = (
            option.get('name'),
            option.get('price'),
            option.get('price_currency'),
        )
        if (
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(price, (str, int, float))
            or isinstance(price, bool)
            or not isinstance(currency, str)
            or len(currency) != 3
            or not currency.isascii()
            or not currency.isalpha()
        ):
            continue
        try:
            amount = Decimal(str(price))
        except (InvalidOperation, ValueError):
            continue
        if not amount.is_finite() or amount < 0:
            continue
        public_option = {'name': name.strip(), 'price': price, 'price_currency': currency.upper()}
        if _valid_url(option.get('url')):
            public_option['url'] = option['url']
        options.append(public_option)
    return options


def public_links(values):
    if not isinstance(values, list):
        return []
    return [
        {'label': link['label'], 'url': link['url']}
        for link in values
        if isinstance(link, dict)
        and isinstance(link.get('label'), str)
        and link['label'].strip()
        and _valid_url(link.get('url'))
    ]
