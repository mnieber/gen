from app.flags import get_flag
from app.settings.dev.inherit import DJANGO_APPS, LOCAL_APPS, THIRD_PARTY_APPS

THIRD_PARTY_APPS += [
    "django_extensions",
    *(["debug_toolbar"] if get_flag("debug_toolbar") else []),
]

LOCAL_APPS += [
    "world.apps.WorldConfig",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
