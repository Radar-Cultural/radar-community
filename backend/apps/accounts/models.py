import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class User(AbstractUser):
    ACCOUNT_PERSON = 'person'
    ACCOUNT_ORGANIZATION = 'organization'
    ACCOUNT_TYPE_CHOICES = [
        (ACCOUNT_PERSON, 'Persona'),
        (ACCOUNT_ORGANIZATION, 'Organización'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('correo electrónico', unique=True)
    account_type = models.CharField(
        'tipo de cuenta',
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=ACCOUNT_PERSON,
        db_index=True,
    )
    public_name = models.CharField('nombre público', max_length=150, blank=True)
    bio = models.TextField('presentación pública', max_length=2000, blank=True)
    is_organizer = models.BooleanField('puede publicar eventos', default=False, db_index=True)
    organizer_enabled_at = models.DateTimeField(null=True, blank=True, editable=False)
    terms_version = models.CharField(max_length=32, blank=True)
    terms_accepted_at = models.DateTimeField(null=True, blank=True, editable=False)

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'persona usuaria'
        verbose_name_plural = 'personas usuarias'

    def save(self, *args, **kwargs):
        self.email = self.email.strip().casefold()
        if self.is_organizer and not self.organizer_enabled_at:
            self.organizer_enabled_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.public_name.strip() or self.get_full_name().strip() or self.username


class OrganizationProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organization_profile',
        limit_choices_to={'account_type': User.ACCOUNT_ORGANIZATION},
    )
    official_name = models.CharField('nombre oficial', max_length=255, unique=True)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField(max_length=5000, blank=True)
    website = models.URLField(blank=True)
    wikidata_id = models.CharField(max_length=32, blank=True)
    same_as = models.URLField(blank=True)
    contact_email = models.EmailField()
    is_verified = models.BooleanField(default=False, db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True, editable=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_organizations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('official_name',)
        verbose_name = 'organización'
        verbose_name_plural = 'organizaciones'

    def __str__(self):
        return self.official_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.official_name)
        if self.is_verified and not self.verified_at:
            self.verified_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def authority_urls(self):
        urls = []
        if self.wikidata_id:
            urls.append(f'https://www.wikidata.org/wiki/{self.wikidata_id}')
        if self.same_as:
            urls.append(self.same_as)
        if self.website:
            urls.append(self.website)
        return list(dict.fromkeys(urls))
