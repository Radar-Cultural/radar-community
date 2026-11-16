import hashlib

from django.utils.text import slugify


def compact_identity_text(value, max_length=255):
    if len(value) <= max_length:
        return value
    digest = hashlib.sha256(value.encode()).hexdigest()[:16]
    return f'{value[: max_length - 17]}-{digest}'


def unique_slug(model, *, value, pk, prefix, max_length):
    base = (slugify(value) or f'{prefix}-{str(pk)[:8]}')[:max_length].strip('-_')
    candidate = base
    counter = 2
    while model.objects.exclude(pk=pk).filter(slug=candidate).exists():
        suffix = f'-{counter}'
        candidate = f'{base[: max_length - len(suffix)].rstrip("-_ ")}{suffix}'
        counter += 1
    return candidate
