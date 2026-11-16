"""Fail deployment checks except for the two consciously deferred HSTS options."""

import os
import sys

import django
from django.core.checks import WARNING, run_checks

DEFERRED_HSTS_WARNINGS = frozenset({'security.W005', 'security.W021'})


def unexpected_issues(messages):
    return [
        message
        for message in messages
        if message.level >= WARNING and message.id not in DEFERRED_HSTS_WARNINGS
    ]


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radar_api.settings')
    django.setup()
    messages = run_checks(include_deployment_checks=True)
    for message in messages:
        print(message, file=sys.stderr if message.level >= WARNING else sys.stdout)
    unexpected = unexpected_issues(messages)
    if unexpected:
        print(f'{len(unexpected)} aviso(s) de despliegue no autorizados.', file=sys.stderr)
        return 1
    print('Comprobación de despliegue: sin avisos nuevos ni errores.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
