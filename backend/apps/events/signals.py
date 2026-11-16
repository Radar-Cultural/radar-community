"""Keep the public event cursor in sync with related editorial changes."""

from django.db.models import Q
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from apps.accounts.models import OrganizationProfile
from apps.catalog.models import Audience, Category, Place

from .models import Event, EventScheduleItem


def _touch_events(event_ids, using):
    Event.objects.using(using).filter(pk__in=event_ids).update(updated_at=timezone.now())


@receiver(pre_save, sender=EventScheduleItem)
def remember_previous_schedule_event(sender, instance, using, **kwargs):
    instance._previous_event_id = (
        sender.objects.using(using)
        .filter(pk=instance.pk)
        .values_list('event_id', flat=True)
        .first()
        if instance.pk
        else None
    )


@receiver(post_save, sender=EventScheduleItem)
def touch_event_after_schedule_save(sender, instance, using, **kwargs):
    event_ids = {instance.event_id, getattr(instance, '_previous_event_id', None)}
    _touch_events(event_ids - {None}, using)


@receiver(post_delete, sender=EventScheduleItem)
def touch_event_after_schedule_delete(sender, instance, using, **kwargs):
    _touch_events((instance.event_id,), using)


def _touch_membership(action, instance, reverse, pk_set, using, relation):
    if action in {'post_add', 'post_remove'}:
        _touch_events(pk_set if reverse else (instance.pk,), using)
    elif action == 'post_clear' and not reverse:
        _touch_events((instance.pk,), using)
    elif action == 'pre_clear' and reverse:
        # post_clear has no pk_set; capture the affected events before the join rows disappear.
        event_ids = (
            Event.objects.using(using).filter(**{relation: instance}).values_list('pk', flat=True)
        )
        _touch_events(event_ids, using)


@receiver(m2m_changed, sender=Event.categories.through)
def touch_events_after_category_membership(
    sender, action, instance, reverse, pk_set, using, **kwargs
):
    _touch_membership(action, instance, reverse, pk_set, using, 'categories')


@receiver(m2m_changed, sender=Event.audiences.through)
def touch_events_after_audience_membership(
    sender, action, instance, reverse, pk_set, using, **kwargs
):
    _touch_membership(action, instance, reverse, pk_set, using, 'audiences')


@receiver(post_save, sender=Category)
@receiver(pre_delete, sender=Category)
def touch_events_after_category_edit(sender, instance, using, **kwargs):
    event_ids = Event.objects.using(using).filter(categories=instance).values_list('pk', flat=True)
    _touch_events(event_ids, using)


@receiver(post_save, sender=Audience)
@receiver(pre_delete, sender=Audience)
def touch_events_after_audience_edit(sender, instance, using, **kwargs):
    event_ids = Event.objects.using(using).filter(audiences=instance).values_list('pk', flat=True)
    _touch_events(event_ids, using)


@receiver(post_save, sender=Place)
def touch_events_after_place_edit(sender, instance, using, **kwargs):
    event_ids = (
        Event.objects.using(using)
        .filter(Q(place_id=instance.pk) | Q(place__parent_id=instance.pk))
        .values_list('pk', flat=True)
    )
    _touch_events(event_ids, using)


@receiver(post_save, sender=OrganizationProfile)
def touch_events_after_organization_edit(sender, instance, using, **kwargs):
    event_ids = (
        Event.objects.using(using).filter(organizer_id=instance.pk).values_list('pk', flat=True)
    )
    _touch_events(event_ids, using)
