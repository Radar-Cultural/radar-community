from django.contrib import admin

from .models import Event, EventContributor, EventScheduleItem, PublicationAcceptance


class EventScheduleInline(admin.TabularInline):
    model = EventScheduleItem
    extra = 0


class EventContributorInline(admin.TabularInline):
    model = EventContributor
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'starts_at',
        'publication_status',
        'visibility_status',
        'event_status',
    )
    list_filter = ('publication_status', 'visibility_status', 'event_status', 'attendance_mode')
    search_fields = ('title', 'summary', 'description', 'external_organizer_name')
    readonly_fields = ('id', 'published_at', 'created_at', 'updated_at')
    filter_horizontal = ('categories', 'audiences')
    inlines = (EventScheduleInline, EventContributorInline)


@admin.register(PublicationAcceptance)
class PublicationAcceptanceAdmin(admin.ModelAdmin):
    list_display = ('event', 'accepted_by', 'terms_version', 'accepted_at')
    readonly_fields = ('accepted_at',)
