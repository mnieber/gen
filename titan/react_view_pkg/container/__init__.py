from pathlib import Path

import moonleap.resource.props as P
from moonleap import (MemFun, Priorities, Prop, create, create_forward,
                      empty_rule, extend, kebab_to_camel, rule)
from moonleap.verbs import has
from titan.react_pkg.packages.use_react_packages import use_react_packages
from titan.react_view_pkg.state.resources import State

from . import props
from .resources import Container

rules = {
    ("container", has, "x+item~list"): empty_rule(),
    ("container", has, "behavior"): empty_rule(),
}


@create("container")
def create_container(term):
    name = kebab_to_camel(term.data)
    container = Container(name=name)
    return container


@rule("container", has, "selection", priority=Priorities.LOW.value)
def container_has_selection(container, selection):
    use_react_packages(
        container.state.state_provider.module.react_app.get_module("utils"),
        ["mergeClickHandlers"],
    )
    return create_forward(container, has, f"{selection.meta.term.data}:highlight")


@rule("container", has, "drag-and-drop", priority=Priorities.LOW.value)
def container_has_drag_and_drop(container, selection):
    return create_forward(container, has, f"{selection.meta.term.data}:insertion")


@rule("state", has, "container")
def state_renders_container(state, container):
    state.renders(
        [container],
        container.name,
        lambda container: dict(container=container),
        [Path(__file__).parent / "templates"],
    )


@extend(State)
class ExtendState:
    containers = P.children(has, "container")


@extend(Container)
class ExtendContainer:
    state = P.parent("state", has)
    named_item_list = P.child(has, "x+item~list")
    named_item = P.child(has, "x+item")
    item = Prop(props.container_item)
    bvrs = P.children(has, "behavior")
    get_bvr = MemFun(props.get_bvr)
