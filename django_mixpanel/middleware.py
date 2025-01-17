
from .track import mixpanel_init
from .track import mixpanel_flush
from ipware import get_client_ip

class DjangoMixpanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != "POST":
            response = self.get_response(request)
            return response

        mixpanel = mixpanel_init(request)
        mixpanel._distinct_id = request.POST.get("mixpanel_distinct_id", None)
        client_ip, is_routable = get_client_ip(request)
        mixpanel._client_ip = client_ip
        request.user.distinct_id = mixpanel._distinct_id
        request.mixpanel = mixpanel

        response = self.get_response(request)
        if response.status_code in (200, 201, 302):
            mixpanel_flush(request, response)

        # Code to be executed for each request/response after
        # the view is called.

        return response
