from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .models import OrganizationProfile, User


@admin.register(User)
class RadarUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Radar Cultural',
            {
                'fields': (
                    'account_type',
                    'public_name',
                    'bio',
                    'is_organizer',
                    'organizer_enabled_at',
                    'terms_version',
                    'terms_accepted_at',
                )
            },
        ),
    )
    readonly_fields = ('organizer_enabled_at', 'terms_accepted_at')
    list_display = ('username', 'email', 'account_type', 'is_organizer', 'is_staff')


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ('official_name', 'is_verified', 'website', 'updated_at')
    list_filter = ('is_verified',)
    search_fields = ('official_name', 'contact_email')
    readonly_fields = ('verified_by', 'verified_at', 'created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if not request.user.has_perm('accounts.verify_organization'):
            return (*fields, 'is_verified')
        return fields

    def save_model(self, request, obj, form, change):
        previous = OrganizationProfile.objects.get(pk=obj.pk) if change else None
        was_verified = previous.is_verified if previous else False
        if obj.is_verified != was_verified:
            if not request.user.has_perm('accounts.verify_organization'):
                raise PermissionDenied('No tienes permiso para verificar organizaciones.')
            if obj.is_verified:
                obj.verified_by = request.user
                obj.verified_at = timezone.now()
            else:
                obj.verified_by = None
                obj.verified_at = None
        elif previous:
            obj.verified_by_id = previous.verified_by_id
            obj.verified_at = previous.verified_at
        if previous:
            obj.user_id = previous.user_id
        super().save_model(request, obj, form, change)
