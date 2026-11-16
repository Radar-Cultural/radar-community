class PublicContentCacheControlMiddleware:
    """Prevent stale public API data after a publication is withdrawn."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path_info
        if (
            path.startswith('/api/v1/')
            or path.startswith('/eventos/')
            or path == '/sitemap.xml'
            or (path.startswith('/sitemap-') and path.endswith('.xml'))
        ):
            response['Cache-Control'] = 'no-store'
        return response
