import moonleap.resource.props as P
from moonleap import extend, kebab_to_snake, tags
from moonleap.utils.case import snake_to_camel
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp

from .resources import AppModule  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    name_snake = kebab_to_snake(term.data)
    module = AppModule(name_snake=name_snake, name=snake_to_camel(name_snake))
    module.output_path = module.name_snake
    return module


@extend(DjangoApp)
class ExtendDjangoApp:
    app_module = P.child(has, "app:module")
