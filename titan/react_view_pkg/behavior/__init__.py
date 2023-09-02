from moonleap import Priorities, create, create_forward, rule, u0
from moonleap.blocks.verbs import has, stores

from .resources import (
    Behavior,
    DeletionBehavior,
    EditBehavior,
    InsertionBehavior,
    StoreBehavior,
)

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


@create("edit:bvr")
def create_edit_behavior(term):
    return EditBehavior(
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


@create("store:bvr")
def create_default_store_behavior(term):
    return StoreBehavior(
        name="store",
        has_param=True,
    )


@create("x:x:bvr")
def create_custom_behavior(term):
    facet_name = term.parts[1]
    if term.parts[0].endswith("-"):
        name = term.parts[0][:-1] + u0(facet_name)
    else:
        name = term.parts[0]

    klass = (
        StoreBehavior
        if facet_name == "store"
        else DeletionBehavior
        if facet_name == "deletion"
        else EditBehavior
        if facet_name == "edit"
        else InsertionBehavior
        if facet_name == "insertion"
        else Behavior
    )
    return klass(
        name=name,
        has_param=False,
        is_skandha=False,
    )


@create("bvr")
def create_behavior(term):
    return Behavior(
        name=term.data,
        has_param=False,
        is_skandha=False,
    )


@rule("container", has + stores, "item~list", priority=Priorities.LOW.value)
def container_has_item_list(container, item_list):
    if not [bvr for bvr in container.bvrs if bvr.facet_name == "store"]:
        return create_forward(container, has, "store:bvr")


@rule("selection:bvr")
def created_selection(selection):
    selection.container.state.module.react_app.set_flags(["app/useMergeHandlers"])


@rule("container", has, "drag-and-drop:bvr")
def container_has_drag_and_drop_behavior(container, bvr):
    return create_forward(container, has, "hovering:bvr")


@rule("container", has, "insertion:bvr")
def container_has_insertion(container, bvr):
    return create_forward(container, has, "display:bvr")


@rule("container", has, "filtering:bvr")
def container_has_filtering(container, bvr):
    return create_forward(container, has, "display:bvr")
