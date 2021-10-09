from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, kebab_to_camel
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import u0
from moonleap.verbs import has, stores
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList
from titan.react_pkg.module import Module
from titan.react_pkg.pkg.jsfilemerger import JsFileMerger

from .props import get_context
from .resources import Store

JsFileMerger.add_pattern("types.ts")

base_tags = [("store", ["component", "react-store"])]


@create("store")
def create_store(term, block):
    store = Store(name=f"{u0(kebab_to_camel(term.data))}Store")
    store.add_template_dir(Path(__file__).parent / "templates", get_context)
    return store


rules = [
    (("store", stores, "item"), empty_rule()),
    (("store", stores, "item~list"), empty_rule()),
]


@extend(Module)
class ExtendModule:
    stores = P.children(has, "store")


@extend(Store)
class ExtendStore(StoreTemplateDirs):
    item_lists_stored = P.children(stores, "item~list")
    items_stored = P.children(stores, "item")


@extend(Item)
class ExtendItem:
    provider_react_stores = P.parents("react-store", stores)
    provider_react_store = P.parent("react-store", stores)


@extend(ItemList)
class ExtendItemList:
    provider_react_stores = P.parents("react-store", stores)
    provider_react_store = P.parent("react-store", stores)
