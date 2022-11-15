from django.urls import path
from django.http import HttpResponse

from uuid import uuid4

from .mixpanel import Events
from .mixpanel import EventProperties
from .mixpanel import ProfileProperties
from django_mixpanel import ProfileMetaProperties
from django_mixpanel.query import MixpanelQuery
from django_mixpanel.track import Settings
from django.conf import settings

import structlog

logger = structlog.get_logger(__name__)

def configure_mixpanel_user(request, email):
    """Configure mixpanel and create/update mixpanel user."""

    fields = {
        "name": "XXXX",
        "website": "https://aaa.com/"
    }
    properties = {ProfileProperties.dollar_email: email}

    if "name" in fields:
        properties[ProfileProperties.dollar_name] = fields["name"]

    if "phone" in fields:
        properties[ProfileProperties.dollar_phone] = fields["phone"]

    # Store users' IP for geolocation purposes
    meta = {ProfileMetaProperties.dollar_ip: request.META["REMOTE_ADDR"]}

    # If Mixpanel profile for given email already exists, use the profile's
    # distinct_id so that this submission is connected to existing user actions
    # stored in Mixpanel
    profile = MixpanelQuery(settings).profile_by_email(email)

    if profile:
        distinct_id = profile["distinct_id"]
    # We haven't seen a user with this email yet, create a new Mixpanel profile
    else:
        distinct_id = request.GET.get("distinct_id")
        if not distinct_id:
            # This should only happen for people with ad blocks. We need to
            # monitorthis number. If it spikes up, it might mean we have a
            # problem with JS execution on form page.
            distinct_id = "m-{}".format(str(uuid4()))
            logger.warning(
                "no distinct_id submitted to form, mixpanel tracking not working",
                distinct_id=distinct_id,
            )

    request.mixpanel.distinct_id = distinct_id

    # Create/Update user profile
    request.mixpanel.profile_set(props=properties, meta=meta)

def track(request):
    email = request.POST["email"]
    configure_mixpanel_user(request, email)
    event_properties = {
        EventProperties.form_name: "Contact Form",
        EventProperties.dollar_email: email,
        EventProperties.dollar_ip: request.META.get('REMOTE_ADDR'),
    }
    request.mixpanel.track(Events.form_submition, event_properties)
    request.mixpanel.track
    return HttpResponse("OK")

urlpatterns = [
    path("track/", track, name="dm-track")
]