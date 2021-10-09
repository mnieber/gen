import moonleap.resource.props as P
from moonleap import create, extend
from moonleap.utils.case import kebab_to_camel, sn
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp

from .resources import AppModule  # noqa


@create("app:module")
def create_app_module(term, block):
    module = AppModule(name=kebab_to_camel(term.data))
    module.output_path = sn(module.name)
    return module


@extend(DjangoApp)
class ExtendDjangoApp:
    app_module = P.child(has, "app:module", required=True)
