from moonleap.utils.case import snake_to_camel, upper0
from moonleap_django.djangoapp.resources import DjangoConfig


def get(module):
    return DjangoConfig(
        {
            "installed_apps": {
                "LOCAL_APPS": [
                    f"{module.name}.apps.{upper0(snake_to_camel(module.name))}Config",
                ],
            },
        }
    )
