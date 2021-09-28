from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel, rule
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import u0
from moonleap.verbs import contains, has
from titan.react_pkg.jsfilemerger import JsFileMerger
from titan.react_pkg.module import Module

from .props import get_context
from .resources import Store

JsFileMerger.add_pattern("types.ts")


@create("store", ["component"])
def create_store(term, block):
    store = Store(name=f"{u0(kebab_to_camel(term.data))}Store")
    store.add_template_dir(Path(__file__).parent / "templates", get_context)
    return store


@rule("store", contains, "item")
def store_contains_item(store, item_list):
    return create_forward(store, contains, f"{item_list.item_name}:item~type")


rules = [(("store", contains, "item~list"), empty_rule())]


@extend(Module)
class ExtendModule:
    stores = P.children(has, "store")


@extend(Store)
class ExtendStore(StoreTemplateDirs):
    item_lists = P.children(contains, "item~list")
