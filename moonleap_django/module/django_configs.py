from moonleap.utils.case import upper0
from moonleap_django.djangoapp.resources import DjangoConfig


def get(module):
    return DjangoConfig(
        {
            "installed_apps": {
                "LOCAL_APPS": [
                    f"{module.name_snake}.apps.{upper0(module.name)}Config",
                ],
            },
        }
    )
