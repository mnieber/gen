import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
)
from moonleap.utils.case import upper0
from moonleap.utils.inflect import plural
from moonleap.verbs import has, uses
from moonleap_react_module.graphqlapi.resources import get_graphql_item_lists
from moonleap_react_state.behavior.resources import Behavior

from . import props
from .resources import ListView, create_load_items_effect


@tags(["list-view"])
def create_list_view(term, block):
    name = kebab_to_camel(term.data)
    list_view = ListView(
        item_name=name, items_name=plural(name), name=f"{upper0(name)}ListView"
    )
    return list_view


@rule("list-view", has, "*", fltr_obj=P.fltr_instance(Behavior))
def list_view_has_a_behavior(list_view, behavior):
    return create_forward(list_view, has, ":behavior", obj_res=behavior)


@rule("list-view")
def maybe_add_load_items_effect_to_list_view(list_view):
    if get_graphql_item_lists(list_view.module.service.api_module, list_view.item_name):
        load_items_effect = create_load_items_effect(list_view)
        return [
            create_forward(
                list_view.module.service.api_module,
                has,
                ":load-items-effect",
                obj_res=load_items_effect,
            ),
            create_forward(
                list_view,
                uses,
                ":load-items-effect",
                obj_res=load_items_effect,
            ),
        ]


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
    load_items_effect = P.child(uses, "load-items-effect")
    behaviors = P.children(has, "behavior")
    p_section_imports = Prop(props.p_section_imports)
    p_section_default_props = Prop(props.p_section_default_props)
    p_section_classnames = Prop(props.p_section_classnames)
    p_section_on_click = Prop(props.p_section_on_click)
