from pathlib import Path

import moonleap.resource.props as P
from moonleap import (MemFun, Prop, add, create, empty_rule, extend,
                      kebab_to_camel, rule)
from moonleap.verbs import has, provides
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList
from titan.react_pkg.module import Module
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.pkg.ml_get import ml_react_app

from . import props, react_app_configs
from .props import get_context
from .resources import State

base_tags = [("state", ["component", "react-state"])]


@create("state")
def create_state(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    state = State(name=name)
    state.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(state, load_node_package_config(__file__))
    return state


@rule("module", has, "state")
def module_has_state(module, state):
    react_app = ml_react_app(module)
    add(react_app, react_app_configs.config)


@extend(Module)
class ExtendModule:
    states = P.children(has, "state")


rules = [
    (("state", provides, "item~list"), empty_rule()),
    (("state", provides, "item"), empty_rule()),
    (("state", provides, "behavior"), empty_rule()),
]


@extend(State)
class ExtendState:
    module = P.parent("module", has)
    behaviors = P.children(provides, "behavior")
    item_lists_provided = P.children(provides, "item~list")
    items_provided = P.children(provides, "item")
    bvrs_by_item_name = Prop(props.bvrs_by_item_name)


@extend(Item)
class ExtendItem:
    provider_react_states = P.parents("react-state", "provides")
    provider_react_state = P.parent("react-state", "provides")


@extend(ItemList)
class ExtendItemList:
    provider_react_states = P.parents("react-state", "provides")
    provider_react_state = P.parent("react-state", "provides")
