from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, create_forward, extend, kebab_to_camel, rule, u0
from moonleap.verbs import has

from . import props, router_configs
from .props import get_context
from .resources import View


@create("view", ["component"])
def create_view(term, block):
    name = u0(kebab_to_camel(term.data))
    view = View(name=f"{name}")
    view.add_template_dir(
        Path(__file__).parent / "templates", get_context, skip_render=props.skip_render
    )
    return view


@create("panel", ["component"])
def create_panel(term, block):
    panel = View(name=f"{u0(term.data)}Panel")
    return panel


@rule("view", has, "panel")
def view_has_panel(view, panel):
    panel.name = view.name + panel.name


@rule("panel", has, "component")
def panel_has_component(panel, component):
    if not component.module:
        return create_forward(panel.parent_view.module, has, component._meta.term)


@extend(View)
class ExtendView:
    create_router_configs = MemFun(router_configs.create_router_configs)
    parent_view = P.parent(View, has)
    left_panel = P.child(has, "left:panel")
    right_panel = P.child(has, "right:panel")
    top_panel = P.child(has, "top:panel")
    bottom_panel = P.child(has, "bottom:panel")
    middle_panel = P.child(has, "middle:panel")
