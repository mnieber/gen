from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, create, empty_rule, extend, kebab_to_camel, rule
from moonleap.verbs import has, provides
from titan.react_pkg.module import Module
from titan.react_pkg.nodepackage import load_node_package_config

from . import props, react_app_configs
from .props import get_context
from .resources import State


@create("state", ["component"])
def create_state(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    state = State(name=name)
    state.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(state, load_node_package_config(__file__))
    return state


@rule("module", has, "state")
def module_has_state(module, state):
    if react_app_configs.config not in module.react_app.react_app_configs.children:
        add(module.react_app, react_app_configs.config)


@extend(Module)
class ExtendModule:
    states = P.children(has, "state")


rules = [
    (("state", provides, "item-list"), empty_rule()),
    (("state", provides, "item"), empty_rule()),
    (("state", provides, "behavior"), empty_rule()),
]


@extend(State)
class ExtendState:
    behaviors = P.children(provides, "behavior")
    item_lists = P.children(provides, "item-list")
    items = P.children(provides, "item")
    bvrs_by_item_name = Prop(props.bvrs_by_item_name)
    store_by_item_name = Prop(props.store_by_item_name)
    type_import_path = MemFun(props.type_import_path)
