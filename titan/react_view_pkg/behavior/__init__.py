from moonleap import create, rule

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
        name="drag-and-drop",
        has_param=True,
    )


@create("editing:bvr")
def create_editing_behavior(term):
    return EditingBehavior(
        name="editing",
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


@rule("selection:bvr")
def created_selection(selection):
    selection.container.state.module.react_app.set_flags(["utils/mergeClickHandlers"])
