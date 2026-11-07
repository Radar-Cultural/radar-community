from django.contrib import admin

from .models import Audience, Category, Place, PlaceAlias


@admin.register(Category, Audience)
class NamedCatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class PlaceAliasInline(admin.TabularInline):
    model = PlaceAlias
    extra = 0


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'locality', 'region', 'is_active')
    list_filter = ('kind', 'is_active', 'country_code')
    search_fields = ('name', 'address', 'locality', 'region', 'aliases__name')
    readonly_fields = ('identity_key', 'normalized_name', 'created_at', 'updated_at')
    inlines = (PlaceAliasInline,)
