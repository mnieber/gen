from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, extend, kebab_to_camel, rule, u0
from moonleap.verbs import has, wraps

from . import props, router_configs
from .props import get_context
from .resources import View

base_tags = [
    ("view", ["component", "react-view"]),
    ("panel", ["view", "react-panel"]),
]


@create("view")
def create_view(term):
    name = u0(kebab_to_camel(term.data + ("view" if term.data.endswith("-") else "")))
    view = View(name=f"{name}")
    view.add_template_dir(Path(__file__).parent / "templates", get_context)
    return view


@rule("view", wraps, "children")
def view_wraps_children(view, children):
    view.wraps_children = True


@create("panel")
def create_panel(term):
    panel = View(name=f"{u0(term.data)}Panel")
    panel.add_template_dir(
        Path(__file__).parent / "templates", get_context, skip_render=props.skip_render
    )
    return panel


@rule("view", has, "panel")
def view_has_panel(view, panel):
    panel.name = view.name + panel.name


@rule("x+view", wraps, "x+component")
def named_view_wraps_named_component(named_view, named_component):
    named_view.typ.wraps_children = True


@extend(View)
class ExtendView:
    create_router_configs = MemFun(router_configs.create_router_configs)
    parent_view = P.parent("view", has)
    left_panel = P.child(has, "x+left:panel")
    right_panel = P.child(has, "x+right:panel")
    top_panel = P.child(has, "x+top:panel")
    bottom_panel = P.child(has, "x+bottom:panel")
    middle_panel = P.child(has, "x+middle:panel")
