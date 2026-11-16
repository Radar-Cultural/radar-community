from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AudienceViewSet,
    CategoryViewSet,
    EventViewSet,
    OrganizationViewSet,
    PlaceViewSet,
    event_calendar_view,
    event_rdf_view,
    event_schema_view,
    status_view,
)

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('categories', CategoryViewSet, basename='category')
router.register('audiences', AudienceViewSet, basename='audience')
router.register('places', PlaceViewSet, basename='place')
router.register('organizations', OrganizationViewSet, basename='organization')

urlpatterns = [
    path('status/', status_view, name='status'),
    path('events/<slug:slug>/schema/', event_schema_view, name='event-schema'),
    path('events/<slug:slug>/schema.rdf', event_rdf_view, name='event-rdf'),
    path('events/<slug:slug>/calendar.ics', event_calendar_view, name='event-calendar'),
    path('', include(router.urls)),
]
