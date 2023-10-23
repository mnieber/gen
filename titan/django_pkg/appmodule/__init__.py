import moonleap.packages.extensions.props as P
from moonleap import create, extend
from moonleap.blocks.verbs import has
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.djangomodule import DjangoModule, create_django_module


@create("app:module")
def create_app_module(term):
    return create_django_module(DjangoModule, term)


@extend(DjangoApp)
class ExtendDjangoApp:
    app_module = P.child(has, "app:module")
