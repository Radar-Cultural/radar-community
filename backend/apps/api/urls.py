from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AudienceViewSet, CategoryViewSet, EventViewSet, PlaceViewSet, status_view

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('categories', CategoryViewSet, basename='category')
router.register('audiences', AudienceViewSet, basename='audience')
router.register('places', PlaceViewSet, basename='place')

urlpatterns = [
    path('status/', status_view, name='status'),
    path('', include(router.urls)),
]
