
from .track import mixpanel_init
from .track import mixpanel_flush

class DjangoMixpanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        mixpanel = mixpanel_init(request)
        request.mixpanel = mixpanel

        response = self.get_response(request)
        if response.status_code in (200, 201):
            mixpanel_flush(request, response)

        # Code to be executed for each request/response after
        # the view is called.

        return response