import moonleap.resource.props as P
from moonleap import (
    MemFun,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    upper0,
)
from moonleap.verbs import has
from moonleap_react_module.store import Store

from . import props
from .resources import LoadItemsEffect


@tags(["load-items-effect"])
def create_loadItemsEffect(term, block):
    item_name = kebab_to_camel(term.data)
    name = f"Load{upper0(item_name)}Effect"
    loadItemsEffect = LoadItemsEffect(item_name=item_name, name=name)
    return loadItemsEffect


@rule("store", has, "load-items-effect")
def store_has_load_items_effect(module, effect):
    pass


@extend(LoadItemsEffect)
class ExtendLoadItemsEffect:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)


@extend(Store)
class ExtendStore:
    load_items_effect = P.child(has, "load-items-effect")
