import moonleap.resource.props as P
from moonleap import Prop, create_forward, extend, kebab_to_camel, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import upper0
from moonleap.verbs import contains, has
from moonleap_react.module import Module

from . import props
from .resources import Store


@tags(["store"])
def create_store(term, block):
    store = Store(name=f"{upper0(kebab_to_camel(term.data))}Store")
    store.add_template_dir(__file__, "templates")
    return store


@rule("module", has, "store")
def create_utils_module(module, store):
    return create_forward(module.service, has, "utils:module")


@rule("module", has, "store")
def add_utils_templates(module, store):
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(Module)
class ExtendModule:
    store = P.child(has, "store")


@extend(Store)
class ExtendStore(StoreTemplateDirs):
    policy_lines = Prop(props.policy_lines)
    item_lists = P.children(contains, "item-list")
    item_types = P.children(contains, "item-type")
    item_list_and_api_pairs = Prop(props.item_list_and_api_pairs)
    apis = Prop(props.apis)
