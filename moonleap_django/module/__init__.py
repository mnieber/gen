import moonleap.resource.props as P
from moonleap import (StoreOutputPaths, add, create_forward, extend,
                      kebab_to_snake, rule, tags)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import snake_to_camel
from moonleap.verbs import has, runs
from moonleap_django.djangoapp import DjangoApp, StoreDjangoConfigs

from . import django_configs
from .resources import Module  # noqa


@tags(["module"])
def create_module(term, block):
    name_snake = kebab_to_snake(term.data)
    module = Module(name_snake=name_snake, name_camel=snake_to_camel(name_snake))
    module.output_path = module.name_snake
    module.add_template_dir(__file__, "templates")
    return module


@rule("module")
def module_created(module):
    add(module, django_configs.get(module))


@rule("django-app", has, "module")
def django_app_has_module(django_app, module):
    module.output_paths.add_source(django_app)
    django_app.django_configs.add_source(module)


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    django_app = P.parent(DjangoApp, has)


@extend(DjangoApp)
class ExtendDjangoApp:
    modules = P.children(has, "module")
