from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.events.models import Event


class StaticSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ('/', '/agenda/', '/codigo-de-conducta/')

    def location(self, item):
        return item


class EventSitemap(Sitemap):
    protocol = 'https'
    limit = 10_000

    def items(self):
        return Event.objects.public().only('slug', 'updated_at').order_by('id')

    def location(self, event):
        return reverse('public-event-page', kwargs={'slug': event.slug})

    def lastmod(self, event):
        return event.updated_at


sitemaps = {'static': StaticSitemap, 'events': EventSitemap}
