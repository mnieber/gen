from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend
from moonleap.blocks.verbs import has
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.djangomodule import create_django_module

from .resources import ApiModule  # noqa


@create("api:module")
def create_api_module(term):
    api_module = create_django_module(ApiModule, term)
    return api_module


@extend(DjangoApp)
class ExtendDjangoApp:
    api_module = P.child(has, "api:module")


rules = {
    "django-app": {
        (has, "api:module"): empty_rule(),
    }
}
