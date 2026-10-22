from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    """301-redirect the bare domain (padev.org) to CANONICAL_HOST (www.padev.org).

    Sevalla serves each custom domain separately and does not redirect between them.
    Other hosts, such as the *.sevalla.app address, are left alone.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        canonical = settings.CANONICAL_HOST
        self.canonical = canonical
        self.bare = canonical.removeprefix('www.') if canonical.startswith('www.') else ''

    def __call__(self, request):
        if self.bare and request.get_host().split(':')[0].lower() == self.bare:
            return HttpResponsePermanentRedirect(f'https://{self.canonical}{request.get_full_path()}')
        return self.get_response(request)
