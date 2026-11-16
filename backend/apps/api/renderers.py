from rest_framework.renderers import BaseRenderer, JSONRenderer


class JsonLdRenderer(JSONRenderer):
    media_type = 'application/ld+json'
    format = 'jsonld'


class RdfXmlRenderer(BaseRenderer):
    media_type = 'application/rdf+xml'
    format = 'rdf'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, bytes):
            return data
        return str(data).encode('utf-8')


class CalendarRenderer(BaseRenderer):
    media_type = 'text/calendar'
    format = 'ics'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, bytes):
            return data
        return str(data).encode(self.charset)
