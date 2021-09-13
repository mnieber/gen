from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    Prop,
    StoreOutputPaths,
    add,
    create,
    create_forward,
    extend,
    kebab_to_camel,
    kebab_to_snake,
    rule,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import snake_to_kebab
from moonleap.verbs import contains, provides, receives
from titan.django_pkg.djangoapp import StoreDjangoConfigs

from . import django_configs, props
from .resources import Module  # noqa


@create(["module"])
def create_module(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    module = Module(name_snake=name_snake, name=name)
    module.output_path = module.name_snake
    module.add_template_dir(Path(__file__).parent / "templates")
    return module


@rule("module")
def module_created(module):
    add(module, django_configs.get(module))


@rule("module", provides, "item-list")
def module_contains_item_list(module, item_list):
    kebab_name = snake_to_kebab(item_list.item_name_snake)
    return create_forward(module, provides, f"{kebab_name}:item-type")


@rule("module", receives, "item")
def module_receives_item(module, item):
    kebab_name = snake_to_kebab(item.item_name_snake)
    return create_forward(module, provides, f"{kebab_name}:item-type")


empty_rules = [("module", contains + provides, "item-type")]


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    item_lists_provided = P.children(provides, "item-list")
    items_received = P.children(receives, "item")
    item_types = P.children(contains + provides, "item-type")
    sections = Prop(props.Sections)
