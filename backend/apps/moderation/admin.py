from django.contrib import admin

from .models import ContentReport, ModerationDecision


class ModerationDecisionInline(admin.TabularInline):
    model = ModerationDecision
    extra = 0
    readonly_fields = (
        'moderator',
        'previous_status',
        'new_status',
        'action',
        'reason',
        'created_at',
    )
    can_delete = False


@admin.register(ContentReport)
class ContentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reason', 'status', 'assigned_to', 'created_at')
    list_filter = ('reason', 'status')
    search_fields = ('details', 'reported_url')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (ModerationDecisionInline,)


@admin.register(ModerationDecision)
class ModerationDecisionAdmin(admin.ModelAdmin):
    list_display = ('report', 'moderator', 'action', 'created_at')
    readonly_fields = (
        'report',
        'moderator',
        'previous_status',
        'new_status',
        'action',
        'reason',
        'previous_visibility',
        'new_visibility',
        'created_at',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
