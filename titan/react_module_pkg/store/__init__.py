import moonleap.resource.props as P
from moonleap import Prop, extend, kebab_to_camel, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import upper0
from moonleap.verbs import contains, has
from titan.react_pkg.jsfilemerger import JsFileMerger
from titan.react_pkg.module import Module

from . import props
from .resources import Store

JsFileMerger.add_pattern("types.ts")


@tags(["store"])
def create_store(term, block):
    store = Store(name=f"{upper0(kebab_to_camel(term.data))}Store")
    store.add_template_dir(__file__, "templates")
    return store


@extend(Module)
class ExtendModule:
    stores = P.children(has, "store")


@extend(Store)
class ExtendStore(StoreTemplateDirs):
    item_lists = P.children(contains, "item-list")
    item_types = P.children(contains, "item-type")
    sections = Prop(props.Sections)
