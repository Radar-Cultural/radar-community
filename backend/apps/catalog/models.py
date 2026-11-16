import hashlib
import unicodedata
import uuid

from django.core.validators import RegexValidator
from django.db import models

from radar_api.identifiers import compact_identity_text, unique_slug


def normalize_catalog_text(value):
    normalized = unicodedata.normalize('NFKD', value or '').casefold()
    characters = []
    latin_base = False
    for char in normalized:
        if unicodedata.category(char).startswith('M'):
            if not latin_base and characters and characters[-1] != ' ':
                characters.append(char)
            continue
        if char.isalnum():
            characters.append(char)
            latin_base = 'LATIN' in unicodedata.name(char, '')
        else:
            characters.append(' ')
            latin_base = False
    return ' '.join(''.join(characters).split())


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
            self.slug = unique_slug(
                self.__class__,
                value=self.name,
                pk=self.pk,
                prefix=self._meta.model_name,
                max_length=self._meta.get_field('slug').max_length,
            )
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
    country_code = models.CharField(
        max_length=2,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]{2}$',
                message='Usa un código de país ISO 3166-1 de dos letras, como MX o FR.',
            )
        ],
        help_text='País del lugar. Indica el código ISO 3166-1 de dos letras.',
    )
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
        self.country_code = self.country_code.upper()
        normalized_name = normalize_catalog_text(self.name)
        self.normalized_name = compact_identity_text(normalized_name)
        identity_source = '|'.join(
            (
                normalized_name,
                normalize_catalog_text(self.address),
                normalize_catalog_text(self.locality),
                normalize_catalog_text(self.region),
                self.country_code,
                str(self.parent_id or 'root'),
            )
        )
        self.identity_key = hashlib.sha256(identity_source.encode()).hexdigest()
        if not self.slug:
            self.slug = unique_slug(
                Place,
                value=self.name,
                pk=self.pk,
                prefix='lugar',
                max_length=self._meta.get_field('slug').max_length,
            )
        super().save(*args, **kwargs)

    @property
    def authority_url(self):
        if self.wikidata_id:
            return f'https://www.wikidata.org/wiki/{self.wikidata_id}'
        return self.same_as


class PlaceAlias(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='aliases')
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, editable=False, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'place aliases'
        constraints = [
            models.UniqueConstraint(
                fields=('place', 'normalized_name'),
                name='unique_place_alias_per_place',
            )
        ]

    def __str__(self):
        return f'{self.name} → {self.place.name}'

    def save(self, *args, **kwargs):
        self.normalized_name = compact_identity_text(normalize_catalog_text(self.name))
        super().save(*args, **kwargs)
