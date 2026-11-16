import re
from uuid import UUID

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.accounts.models import OrganizationProfile
from apps.catalog.models import Audience, Category, Place
from apps.events.models import Event
from apps.events.services.calendar import render_event_calendar
from apps.events.services.rdf import render_event_rdf
from apps.events.services.semantic import build_event_schema

from .renderers import CalendarRenderer, JsonLdRenderer, RdfXmlRenderer
from .serializers import (
    AudienceSerializer,
    CategorySerializer,
    EventSerializer,
    OrganizationSerializer,
    PlaceSerializer,
)


class PublicReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('get', 'head', 'options')


class CategoryViewSet(PublicReadOnlyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True).order_by('sort_order', 'name')


class AudienceViewSet(PublicReadOnlyViewSet):
    serializer_class = AudienceSerializer
    queryset = Audience.objects.filter(is_active=True).order_by('sort_order', 'name')


class PlaceViewSet(PublicReadOnlyViewSet):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        queryset = Place.objects.filter(is_active=True).order_by('name')
        query = self.request.query_params.get('q', '').strip()
        if len(query) > 120:
            raise ValidationError({'q': 'La búsqueda no puede exceder 120 caracteres.'})
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(address__icontains=query)
                | Q(locality__icontains=query)
                | Q(region__icontains=query)
                | Q(aliases__name__icontains=query)
            ).distinct()
        return queryset


class OrganizationViewSet(PublicReadOnlyViewSet):
    serializer_class = OrganizationSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = OrganizationProfile.objects.filter(is_verified=True).order_by('official_name')
        query = self.request.query_params.get('q', '').strip()
        if len(query) > 120:
            raise ValidationError({'q': 'La búsqueda no puede exceder 120 caracteres.'})
        if query:
            queryset = queryset.filter(
                Q(official_name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


class EventViewSet(PublicReadOnlyViewSet):
    serializer_class = EventSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = (
            Event.objects.public()
            .select_related('place', 'place__parent', 'organizer')
            .prefetch_related('categories', 'audiences', 'schedule_items')
            .order_by('starts_at', 'title')
        )
        params = self.request.query_params
        query = params.get('q', '').strip()
        if len(query) > 120:
            raise ValidationError({'q': 'La búsqueda no puede exceder 120 caracteres.'})
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(description__icontains=query)
            )
        if category := self._slug_filter(params, 'category', 180):
            queryset = queryset.filter(categories__slug=category)
        if audience := self._slug_filter(params, 'audience', 180):
            queryset = queryset.filter(audiences__slug=audience)
        if place := params.get('place', '').strip():
            if len(place) > 36:
                raise ValidationError({'place': 'Usa un UUID válido para el lugar.'})
            try:
                place_id = UUID(place)
            except ValueError as error:
                raise ValidationError({'place': 'Usa un UUID válido para el lugar.'}) from error
            queryset = queryset.filter(place_id=place_id)
        start = params.get('from', '').strip()
        end = params.get('to', '').strip()
        start_at = self._parse_datetime(start, 'from') if start else None
        end_at = self._parse_datetime(end, 'to') if end else None
        if start_at and end_at and end_at < start_at:
            raise ValidationError({'to': 'Debe ser igual o posterior a from.'})
        if start_at:
            queryset = queryset.filter(starts_at__gte=start_at)
        if not_finished_at := params.get('not_finished_at', '').strip():
            instant = self._parse_datetime(not_finished_at, 'not_finished_at')
            queryset = queryset.filter(
                Q(starts_at__gte=instant)
                | Q(ends_at__gte=instant)
                | Q(schedule_items__starts_at__gte=instant)
                | Q(schedule_items__ends_at__gte=instant)
            )
        if end_at:
            queryset = queryset.filter(starts_at__lte=end_at)
        if updated_since := params.get('updated_since', '').strip():
            queryset = queryset.filter(
                updated_at__gte=self._parse_datetime(updated_since, 'updated_since')
            )
        if organizer := self._slug_filter(params, 'organizer', 280):
            queryset = queryset.filter(organizer__slug=organizer, organizer__is_verified=True)
        if (has_image := params.get('has_image')) is not None:
            value = has_image.strip().lower()
            if value not in {'true', 'false'}:
                raise ValidationError({'has_image': 'Usa true o false.'})
            image_available = (
                Q(include_image_in_open_data=True)
                & ~Q(image_url='')
                & Q(image_license__in=(Event.IMAGE_CC0, Event.IMAGE_CC_BY, Event.IMAGE_CC_BY_SA))
            )
            queryset = (
                queryset.filter(image_available)
                if value == 'true'
                else queryset.exclude(image_available)
            )
        if status := params.get('status', '').strip():
            allowed_statuses = {value for value, _label in Event.STATUS_CHOICES}
            if status not in allowed_statuses:
                raise ValidationError({'status': 'Usa un estado Schema.org permitido.'})
            queryset = queryset.filter(event_status=status)
        if attendance_mode := params.get('attendance_mode', '').strip():
            allowed_modes = {value for value, _label in Event.ATTENDANCE_CHOICES}
            if attendance_mode not in allowed_modes:
                raise ValidationError({'attendance_mode': 'Usa una modalidad permitida.'})
            queryset = queryset.filter(attendance_mode=attendance_mode)
        ordering = params.get('ordering', 'starts_at').strip()
        allowed_ordering = {'starts_at', '-starts_at', 'updated_at', '-updated_at'}
        if ordering not in allowed_ordering:
            raise ValidationError({'ordering': 'Usa un orden permitido por el contrato.'})
        return queryset.distinct().order_by(ordering, 'id')

    @staticmethod
    def _slug_filter(params, field, max_length):
        value = params.get(field, '').strip()
        if value and (len(value) > max_length or not re.fullmatch(r'[-a-zA-Z0-9_]+', value)):
            raise ValidationError({field: 'Usa un slug ASCII válido y dentro del límite.'})
        return value

    @staticmethod
    def _parse_datetime(value, field):
        if len(value) > 64:
            raise ValidationError({field: 'La fecha y hora supera 64 caracteres.'})
        parsed = parse_datetime(value)
        if parsed is None:
            raise ValidationError({field: 'Usa una fecha y hora válida en formato ISO 8601.'})
        if parsed.utcoffset() is None:
            raise ValidationError({field: 'Incluye la zona horaria: Z o un offset ISO 8601.'})
        return parsed


@api_view(['GET', 'HEAD'])
@permission_classes([permissions.AllowAny])
def status_view(_request):
    return Response({'status': 'ok', 'service': 'radar-cultural-api', 'version': 'v1'})


def _public_event(slug):
    queryset = (
        Event.objects.public()
        .select_related('place', 'place__parent', 'organizer')
        .prefetch_related('categories', 'audiences', 'schedule_items')
    )
    return get_object_or_404(queryset, slug=slug)


@api_view(['GET', 'HEAD'])
@permission_classes([permissions.AllowAny])
@renderer_classes([JsonLdRenderer])
def event_schema_view(request, slug):
    return Response(build_event_schema(_public_event(slug), request))


@api_view(['GET', 'HEAD'])
@permission_classes([permissions.AllowAny])
@renderer_classes([RdfXmlRenderer])
def event_rdf_view(request, slug):
    content = render_event_rdf(build_event_schema(_public_event(slug), request))
    return Response(content)


@api_view(['GET', 'HEAD'])
@permission_classes([permissions.AllowAny])
@renderer_classes([CalendarRenderer])
def event_calendar_view(request, slug):
    event = _public_event(slug)
    event_url = request.build_absolute_uri(f'/api/v1/events/{event.slug}/')
    response = Response(render_event_calendar(event, event_url))
    response['Content-Disposition'] = f'inline; filename="{event.slug}.ics"'
    return response
