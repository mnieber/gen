import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    create_forward,
    extend,
    kebab_to_camel,
    rule,
    tags,
    upper0,
)
from moonleap.verbs import has, shows

from . import props, router_configs
from .resources import View


@tags(["view"])
def create_view(term, block):
    name = upper0(kebab_to_camel(term.data))
    view = View(name=f"{name}View")
    return view


@tags(["panel"])
def create_panel(term, block):
    panel = View(name=f"{upper0(term.data)}Panel")
    return panel


@rule("view", has, "panel")
def view_has_panel(view, panel):
    panel.name = view.name + panel.name
    return [
        create_forward(panel, "is-subpanel-of", ":parent-view", obj_res=view),
        create_forward(view.module, has, ":component", panel),
    ]


@rule("view", shows, "children")
def view_wraps_children(term, block):
    pass


@extend(View)
class ExtendView:
    render = MemFun(props.render)
    create_router_configs = MemFun(router_configs.create_router_configs)
    wraps_children = P.child(shows, ":children")
    parent_view = P.child("is-subpanel-of", ":parent-view")
    left_panel = P.child(has, "left:panel")
    right_panel = P.child(has, "right:panel")
    top_panel = P.child(has, "top:panel")
    bottom_panel = P.child(has, "bottom:panel")
    middle_panel = P.child(has, "middle:panel")
    sections = Prop(props.Sections)
