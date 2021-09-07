from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    StoreOutputPaths,
    StoreTemplateDirs,
    add,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    kebab_to_snake,
    rule,
)
from moonleap.utils.case import snake_to_kebab
from moonleap.verbs import contains, provides
from titan.django_pkg.djangoapp import StoreDjangoConfigs

from . import django_configs
from .props import get_context
from .resources import Module  # noqa


@create("module", [])
def create_module(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    module = Module(name_snake=name_snake, name=name)
    module.output_path = module.name_snake
    module.add_template_dir(Path(__file__).parent / "templates", get_context)
    return module


@rule("module")
def module_created(module):
    add(module, django_configs.get(module))


@rule("module", provides, "item-list")
def module_contains_item_list(module, item_list):
    kebab_name = snake_to_kebab(item_list.item_name_snake)
    return create_forward(module, provides, f"{kebab_name}:item-type")


rules = [(("module", contains + provides, "item-type"), empty_rule())]


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    item_lists_provided = P.children(provides, "item-list")
    item_types = P.children(contains + provides, "item-type")
