import hashlib
import re
import unicodedata
import uuid

from django.db import models
from django.utils.text import slugify


def normalize_catalog_text(value):
    normalized = unicodedata.normalize('NFKD', value or '').casefold()
    normalized = ''.join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r'[^a-z0-9]+', ' ', normalized).strip()


class NamedCatalog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ('sort_order', 'name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(NamedCatalog):
    schema_type = models.CharField(
        max_length=120,
        blank=True,
        help_text='Tipo o identificador interoperable cuando exista una equivalencia verificable.',
    )

    class Meta(NamedCatalog.Meta):
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'


class Audience(NamedCatalog):
    wikidata_id = models.CharField(max_length=32, blank=True)

    class Meta(NamedCatalog.Meta):
        verbose_name = 'público objetivo'
        verbose_name_plural = 'públicos objetivo'


class Place(models.Model):
    KIND_VENUE = 'venue'
    KIND_CAMPUS = 'campus'
    KIND_BUILDING = 'building'
    KIND_ROOM = 'room'
    KIND_OUTDOOR = 'outdoor'
    KIND_ONLINE = 'online'
    KIND_OTHER = 'other'
    KIND_CHOICES = [
        (KIND_VENUE, 'Recinto'),
        (KIND_CAMPUS, 'Campus o complejo'),
        (KIND_BUILDING, 'Edificio'),
        (KIND_ROOM, 'Sala o salón'),
        (KIND_OUTDOOR, 'Espacio abierto'),
        (KIND_ONLINE, 'Espacio en línea'),
        (KIND_OTHER, 'Otro'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    kind = models.CharField(max_length=16, choices=KIND_CHOICES, default=KIND_VENUE)
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='contained_places',
    )
    address = models.CharField(max_length=500, blank=True)
    locality = models.CharField(max_length=160, blank=True)
    region = models.CharField(max_length=160, blank=True)
    country_code = models.CharField(max_length=2, default='MX')
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    wikidata_id = models.CharField(max_length=32, blank=True)
    same_as = models.URLField(blank=True)
    normalized_name = models.CharField(max_length=255, editable=False, db_index=True)
    identity_key = models.CharField(max_length=64, unique=True, editable=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=('is_active', 'name'), name='place_active_name_idx'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_catalog_text(self.name)
        identity_source = '|'.join(
            (
                self.normalized_name,
                normalize_catalog_text(self.address),
                normalize_catalog_text(self.locality),
                str(self.parent_id or 'root'),
            )
        )
        self.identity_key = hashlib.sha256(identity_source.encode()).hexdigest()
        if not self.slug:
            base = slugify(self.name) or f'lugar-{str(self.id)[:8]}'
            candidate = base
            counter = 2
            while Place.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f'{base}-{counter}'
                counter += 1
            self.slug = candidate
        self.country_code = self.country_code.upper()
        super().save(*args, **kwargs)

    @property
    def authority_url(self):
        if self.wikidata_id:
            return f'https://www.wikidata.org/wiki/{self.wikidata_id}'
        return self.same_as


class PlaceAlias(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='aliases')
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, unique=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'place aliases'

    def __str__(self):
        return f'{self.name} → {self.place.name}'

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_catalog_text(self.name)
        super().save(*args, **kwargs)
