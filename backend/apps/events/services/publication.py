from django.core.exceptions import PermissionDenied

from apps.events.models import Event

ALLOWED_TRANSITIONS = {
    Event.PUBLICATION_DRAFT: {Event.PUBLICATION_REVIEW},
    Event.PUBLICATION_REVIEW: {Event.PUBLICATION_DRAFT, Event.PUBLICATION_PUBLISHED},
    Event.PUBLICATION_PUBLISHED: {Event.PUBLICATION_REVIEW, Event.PUBLICATION_ARCHIVED},
    Event.PUBLICATION_ARCHIVED: {Event.PUBLICATION_DRAFT},
}


def authorize_publication_transition(*, previous_status, new_status, actor):
    if previous_status is None:
        if new_status != Event.PUBLICATION_DRAFT:
            raise PermissionDenied('Crea el evento como borrador.')
        return False
    if previous_status == new_status:
        if new_status == Event.PUBLICATION_PUBLISHED and not actor.has_perm('events.publish_event'):
            raise PermissionDenied('No tienes permiso para editar un evento publicado.')
        return False
    if new_status not in ALLOWED_TRANSITIONS.get(previous_status, set()):
        raise PermissionDenied('Transición editorial no permitida.')
    if previous_status == Event.PUBLICATION_PUBLISHED or new_status == Event.PUBLICATION_PUBLISHED:
        if not actor.has_perm('events.publish_event'):
            raise PermissionDenied('No tienes permiso para publicar o retirar un evento.')
    elif previous_status != Event.PUBLICATION_DRAFT and not actor.has_perm('events.review_event'):
        raise PermissionDenied('No tienes permiso para revisar eventos.')
    return True
