from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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
    readonly_fields = ('created_at', 'updated_at', 'verified_at')
