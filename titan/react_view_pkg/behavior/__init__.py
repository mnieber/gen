from moonleap import create, create_forward, rule, u0
from moonleap.blocks.verbs import has

from .resources import Behavior, DeletionBehavior, EditingBehavior, InsertionBehavior

base_tags = {}

rules = {}


@create("addition:bvr")
def create_addition_behavior(term):
    return Behavior(
        name="addition",
        has_param=True,
    )


@create("deletion:bvr")
def create_deletion_behavior(term):
    return DeletionBehavior(
        name="deletion",
        has_param=False,
    )


@create("drag-and-drop:bvr")
def create_drag_and_drop_behavior(term):
    return Behavior(
        name="dragAndDrop",
        has_param=False,
    )


@create("editing:bvr")
def create_editing_behavior(term):
    return EditingBehavior(
        name="edit",
        has_param=False,
    )


@create("filtering:bvr")
def create_filtering_behavior(term):
    return Behavior(
        name="filtering",
        has_param=False,
    )


@create("highlight:bvr")
def create_highlight_behavior(term):
    return Behavior(
        name="highlight",
        has_param=True,
    )


@create("hovering:bvr")
def create_hovering_behavior(term):
    return Behavior(
        name="hovering",
        has_param=False,
    )


@create("insertion:bvr")
def create_insertion_behavior(term):
    return InsertionBehavior(
        name="insertion",
        has_param=True,
    )


@create("selection:bvr")
def create_selection_behavior(term):
    return Behavior(
        name="selection",
        has_param=True,
    )


@create("x:store:bvr")
def create_selection_behavior(term):
    if term.parts[0].endswith("-"):
        name = term.parts[0][:-1] + u0(term.parts[1])
    else:
        name = term.parts[0]
    return Behavior(
        name=name,
        has_param=False,
    )


@create("bvr")
def create_behavior(term):
    return Behavior(
        name=term.data,
        has_param=False,
        is_skandha=False,
    )


@rule("selection:bvr")
def created_selection(selection):
    selection.container.state.module.react_app.set_flags(["utils/mergeClickHandlers"])


@rule("container", has, "drag-and-drop:bvr")
def container_has_drag_and_drop_behavior(container, bvr):
    return create_forward(container, has, "hovering:bvr")
