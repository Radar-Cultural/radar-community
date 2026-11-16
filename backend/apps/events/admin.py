from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db import transaction

from .models import (
    Event,
    EventContributor,
    EventPublicationDecision,
    EventScheduleItem,
    PublicationAcceptance,
)
from .services.publication import ALLOWED_TRANSITIONS, authorize_publication_transition


class EventScheduleInline(admin.TabularInline):
    model = EventScheduleItem
    extra = 0


class EventContributorInline(admin.TabularInline):
    model = EventContributor
    extra = 0


class EventPublicationDecisionInline(admin.TabularInline):
    model = EventPublicationDecision
    extra = 0
    can_delete = False
    readonly_fields = ('actor', 'previous_status', 'new_status', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


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
    readonly_fields = (
        'id',
        'created_by',
        'published_by',
        'published_at',
        'visibility_status',
        'created_at',
        'updated_at',
    )
    filter_horizontal = ('categories', 'audiences')
    inlines = (EventScheduleInline, EventContributorInline, EventPublicationDecisionInline)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        field = form.base_fields.get('publication_status')
        if field is None:
            return form
        current_status = obj.publication_status if obj else None
        allowed = {current_status} if current_status else {Event.PUBLICATION_DRAFT}
        for candidate in ALLOWED_TRANSITIONS.get(current_status, set()):
            try:
                authorize_publication_transition(
                    previous_status=current_status,
                    new_status=candidate,
                    actor=request.user,
                )
            except PermissionDenied:
                continue
            allowed.add(candidate)
        field.choices = [(value, label) for value, label in field.choices if value in allowed]
        return form

    def has_change_permission(self, request, obj=None):
        if obj and obj.publication_status == Event.PUBLICATION_PUBLISHED:
            if not request.user.has_perm('events.publish_event'):
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        previous = None
        if change:
            previous = (
                Event.objects.select_for_update()
                .only(
                    'publication_status',
                    'visibility_status',
                    'created_by',
                    'published_by',
                    'published_at',
                )
                .get(pk=obj.pk)
            )
        previous_status = previous.publication_status if previous else None
        changed_status = authorize_publication_transition(
            previous_status=previous_status,
            new_status=obj.publication_status,
            actor=request.user,
        )
        if not change:
            obj.created_by = request.user
            obj.published_by = None
            obj.published_at = None
        else:
            obj.created_by_id = previous.created_by_id
            obj.visibility_status = previous.visibility_status
            obj.published_by_id = previous.published_by_id
            obj.published_at = previous.published_at
        if changed_status and obj.publication_status == Event.PUBLICATION_PUBLISHED:
            obj.published_by = request.user
        super().save_model(request, obj, form, change)
        if changed_status:
            EventPublicationDecision.objects.create(
                event=obj,
                actor=request.user,
                previous_status=previous_status,
                new_status=obj.publication_status,
            )


@admin.register(PublicationAcceptance)
class PublicationAcceptanceAdmin(admin.ModelAdmin):
    list_display = ('event', 'accepted_by', 'terms_version', 'conduct_version', 'accepted_at')
    readonly_fields = (
        'event',
        'accepted_by',
        'terms_version',
        'conduct_version',
        'description_license',
        'confirms_accuracy',
        'confirms_rights',
        'accepted_at',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EventPublicationDecision)
class EventPublicationDecisionAdmin(admin.ModelAdmin):
    list_display = ('event', 'actor', 'previous_status', 'new_status', 'created_at')
    readonly_fields = ('event', 'actor', 'previous_status', 'new_status', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
