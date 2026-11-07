from uuid import UUID

from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.catalog.models import Audience, Category, Place
from apps.events.models import Event

from .serializers import AudienceSerializer, CategorySerializer, EventSerializer, PlaceSerializer


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


class EventViewSet(PublicReadOnlyViewSet):
    serializer_class = EventSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = (
            Event.objects.public()
            .select_related('place', 'organizer')
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
        if category := params.get('category', '').strip():
            queryset = queryset.filter(categories__slug=category)
        if audience := params.get('audience', '').strip():
            queryset = queryset.filter(audiences__slug=audience)
        if place := params.get('place', '').strip():
            try:
                place_id = UUID(place)
            except ValueError as error:
                raise ValidationError({'place': 'Usa un UUID válido para el lugar.'}) from error
            queryset = queryset.filter(place_id=place_id)
        if start := params.get('from', '').strip():
            queryset = queryset.filter(starts_at__gte=self._parse_datetime(start, 'from'))
        if end := params.get('to', '').strip():
            queryset = queryset.filter(starts_at__lte=self._parse_datetime(end, 'to'))
        return queryset.distinct()

    @staticmethod
    def _parse_datetime(value, field):
        parsed = parse_datetime(value)
        if parsed is None:
            raise ValidationError({field: 'Usa una fecha y hora válida en formato ISO 8601.'})
        if timezone.is_naive(parsed):
            parsed = timezone.make_aware(parsed)
        return parsed


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def status_view(_request):
    return Response({'status': 'ok', 'service': 'radar-cultural-api', 'version': 'v1'})
