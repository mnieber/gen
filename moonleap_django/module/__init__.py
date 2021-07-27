import moonleap.resource.props as P
from moonleap import (
    StoreOutputPaths,
    add,
    create_forward,
    extend,
    kebab_to_snake,
    rule,
    tags,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has, runs
from moonleap_django.djangoapp import DjangoApp, StoreDjangoConfigs

from . import django_configs
from .resources import Module  # noqa


@tags(["module"])
def create_module(term, block):
    module = Module(name=kebab_to_snake(term.data))
    module.output_path = module.name
    return module


@rule("module")
def module_created(module):
    add(module, django_configs.get(module))


@rule("django-app", has, "module")
def django_app_has_module(django_app, module):
    module.output_paths.add_source(django_app)
    django_app.django_configs.add_source(module)


@rule("service", runs, "django-app")
def service_runs_django_app(service, django_app):
    return create_forward(django_app, has, "app:module")


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    django_app = P.parent(DjangoApp, has)


@extend(DjangoApp)
class ExtendDjangoApp:
    modules = P.children(has, "module")
