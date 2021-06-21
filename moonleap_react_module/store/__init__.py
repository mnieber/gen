import moonleap.resource.props as P
from moonleap import Prop, extend, kebab_to_camel, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import upper0
from moonleap.verbs import contains, has
from moonleap_react.jsfilemerger import JsFileMerger
from moonleap_react.module import Module

from . import props
from .resources import Store

JsFileMerger.add_pattern("types.ts")


@tags(["store"])
def create_store(term, block):
    store = Store(name=f"{upper0(kebab_to_camel(term.data))}Store")
    store.add_template_dir(__file__, "templates")
    return store


@rule("module", has, "store")
def add_utils_templates(module, store):
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(Module)
class ExtendModule:
    stores = P.children(has, "store")


@extend(Store)
class ExtendStore(StoreTemplateDirs):
    item_lists = P.children(contains, "item-list")
    item_types = P.children(contains, "item-type")
    construct_item_lists_section = Prop(props.construct_item_lists_section)
    on_load_data_section = Prop(props.on_load_data_section)
