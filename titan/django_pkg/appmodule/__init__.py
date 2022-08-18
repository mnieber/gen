from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, empty_rule, extend
from moonleap.verbs import has
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.djangomodule import DjangoModule

rules = [(("app:module", has, "graphql:app"), empty_rule())]


@create("app:module")
def create_app_module(term):
    app_module = DjangoModule(name="app")
    app_module.template_dir = Path(__file__).parent / "templates"
    app_module.template_context = dict(app_module=app_module)
    return app_module


@extend(DjangoApp)
class ExtendDjangoApp:
    app_module = P.child(has, "app:module")
