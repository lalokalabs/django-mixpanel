"""Mixpanel tracking.
Uses https://github.com/lalokalabs/django-mixpanel.
"""

from dataclasses import dataclass
from django.http import HttpRequest
from django_mixpanel import Event
from django_mixpanel import EventProperties as BaseEventProperties
from django_mixpanel import Events as BaseEvents
from django_mixpanel import ProfileProperties as BaseProfileProperties
from django_mixpanel import Property
from django_mixpanel.consumer import MockedConsumer
#from django_mixpanel.track import mixpanel_flush
from django_mixpanel.track import mixpanel_init
from django_mixpanel.track import MixpanelTrack

import structlog

logger = structlog.get_logger(__name__)


@dataclass(frozen=True)
class Events(BaseEvents):
    """Minisites specific events on top of pyramid_mixpanel Events."""

    form_submition: Event = Event("Form Submitted")
    kafkai_articles: Event = Event("Kafkai Live Articles Requested")
    pareto_update: Event = Event("Pareto Update Check")
    pareto_setapp_email: Event = Event("Pareto Setapp Email")


@dataclass(frozen=True)
class EventProperties(BaseEventProperties):
    """Minisites specific event properties on top of pyramid_mixpanel Events.
    Since email and ip are the only properties we are capturing during
    the time of form_submition event, hence we are adding them as event properties.
    """

    dollar_email: Property = Property("$email")
    dollar_ip: Property = Property("$ip")
    form_name: Property = Property("form_name")

    # Kafkai articles
    niche: Property = Property("niche")
    article_count: Property = Property("article_count")

    # ParetoApp
    app_version: Property = Property("app_version")
    os_version: Property = Property("os_version")
    distribution: Property = Property("distribution")


@dataclass(frozen=True)
class ProfileProperties(BaseProfileProperties):
    """Minisites specific ProfileProperties on top of pyramid_mixpanel ProfileProperties."""

    minisite_forms_submitted: Property = Property("minisite_forms_submitted")