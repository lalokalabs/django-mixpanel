from pytest_djangoapp import configure_djangoapp_plugin

pytest_plugins = configure_djangoapp_plugin({
        "MIXPANEL_EVENTS": "django_mixpanel.tests.testapp.mixpanel.Events",
        "MIXPANEL_EVENT_PROPERTIES": "django_mixpanel.tests.testapp.mixpanel.EventProperties",
        "MIXPANEL_PROFILE_PROPERTIES": "django_mixpanel.tests.testapp.mixpanel.ProfileProperties",
        "MIXPANEL_PROFILE_META_PROPERTIES": "django_mixpanel.ProfileMetaProperties",
        "MIXPANEL_TOKEN": False,
        "MIXPANEL_API_SECRET": "xxxx",
    },
    migrate=False,
    extend_MIDDLEWARE=[
        'django_mixpanel.middleware.DjangoMixpanelMiddleware',
    ],
)