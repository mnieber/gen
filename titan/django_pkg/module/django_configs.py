from moonleap.utils.case import u0
from titan.django_pkg.djangoapp.resources import DjangoConfig


def get(module):
    return DjangoConfig(
        {
            "installed_apps": {
                "LOCAL_APPS": [
                    f"{module.name_snake}.apps.{u0(module.name)}Config",
                ],
            },
        }
    )
