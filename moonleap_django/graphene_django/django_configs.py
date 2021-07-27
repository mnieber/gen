from moonleap import chop0
from moonleap_django.djangoapp.resources import DjangoConfig


def get():
    return DjangoConfig(
        {
            "installed_apps": {
                "THIRD_PARTY_APPS": [
                    "graphene_django",
                ],
            },
        }
    )
