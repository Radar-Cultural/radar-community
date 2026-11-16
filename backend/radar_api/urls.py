from django.contrib import admin
from django.contrib.sitemaps.views import index as sitemap_index
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.events.views import public_event_page
from radar_api.sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.urls')),
    path('eventos/<slug:slug>/', public_event_page, name='public-event-page'),
    path('sitemap.xml', sitemap_index, {'sitemaps': sitemaps}, name='sitemap-index'),
    path(
        'sitemap-<section>.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
]
