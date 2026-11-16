from django.contrib import admin

from .models import ContentReport, ModerationDecision
from .services import record_moderation_decision


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
    readonly_fields = ('reporter', 'status', 'assigned_to', 'created_at', 'updated_at')
    inlines = (ModerationDecisionInline,)

    def save_model(self, request, obj, form, change):
        if change:
            previous = ContentReport.objects.only('reporter', 'status', 'assigned_to').get(
                pk=obj.pk
            )
            obj.reporter_id = previous.reporter_id
            obj.status = previous.status
            obj.assigned_to_id = previous.assigned_to_id
        else:
            obj.reporter = request.user
            obj.status = ContentReport.STATUS_SUBMITTED
            obj.assigned_to = None
        super().save_model(request, obj, form, change)


@admin.register(ModerationDecision)
class ModerationDecisionAdmin(admin.ModelAdmin):
    list_display = ('report', 'moderator', 'action', 'created_at')
    fields = (
        'report',
        'action',
        'reason',
        'moderator',
        'previous_status',
        'new_status',
        'previous_visibility',
        'new_visibility',
        'created_at',
    )
    readonly_fields = (
        'moderator',
        'previous_status',
        'new_status',
        'previous_visibility',
        'new_visibility',
        'created_at',
    )

    def has_add_permission(self, request):
        return request.user.has_perm('moderation.review_content_reports')

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        decision = record_moderation_decision(
            report=obj.report,
            moderator=request.user,
            action=obj.action,
            reason=obj.reason,
        )
        obj.pk = decision.pk
        obj.moderator = decision.moderator
        obj.previous_status = decision.previous_status
        obj.new_status = decision.new_status
        obj.previous_visibility = decision.previous_visibility
        obj.new_visibility = decision.new_visibility
        obj.created_at = decision.created_at
