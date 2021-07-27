import moonleap.resource.props as P
from moonleap import extend, kebab_to_snake, tags
from moonleap.verbs import has
from moonleap_django.djangoapp import DjangoApp

from .resources import AppModule  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=kebab_to_snake(term.data))
    return module


@extend(DjangoApp)
class ExtendDjangoApp:
    app_module = P.child(has, "app:module")
