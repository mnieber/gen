from pathlib import Path

import moonleap.resource.props as P
from moonleap import Prop, create, create_forward, extend, kebab_to_camel, rule
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import upper0
from moonleap.verbs import contains, has
from titan.react_pkg.jsfilemerger import JsFileMerger
from titan.react_pkg.module import Module

from . import props
from .resources import Store

JsFileMerger.add_pattern("types.ts")


@create(["store"])
def create_store(term, block):
    store = Store(name=f"{upper0(kebab_to_camel(term.data))}Store")
    store.add_template_dir(Path(__file__).parent / "templates")
    return store


@rule("store", contains, "item")
def store_contains_item(store, item_list):
    return create_forward(store, contains, f"{item_list.item_name}:item-type")


@rule("store", contains, "item-list")
def store_contains_item_list(store, item_list):
    return create_forward(store, contains, f"{item_list.item_name}:item-type")


@extend(Module)
class ExtendModule:
    stores = P.children(has, "store")


@extend(Store)
class ExtendStore(StoreTemplateDirs):
    item_lists = P.children(contains, "item-list")
    item_types = P.children(contains, "item-type")
    sections = Prop(props.Sections)
