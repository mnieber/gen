from moonleap.utils.case import sn, u0
from titan.django_pkg.djangoapp.resources import DjangoConfig


def get(module):
    return DjangoConfig(
        {
            "installed_apps": {
                "LOCAL_APPS": [
                    f"{sn(module.name)}.apps.{u0(module.name)}Config",
                ],
            },
        }
    )
