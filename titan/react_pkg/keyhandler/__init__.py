
import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, extend
from moonleap.blocks.verbs import has
from moonleap.packages.rule import Priorities

from .resources import KeyHandler

base_tags = {
    "key-handler": ["component", "react-view"],
}


@create("key-handler")
def create_key_handler(term):
    view = KeyHandler(name="KeyHandler")
    return view


def list_view_has_key_handler(list_view, key_handler):
    if not key_handler.module:
        return create_forward(list_view.module, has, key_handler)


@extend(KeyHandler)
class ExtendKeyHandler:
    list_view = P.parent("list-view", has)


rules = {
    "list-view": {
        (has, "key-handler", Priorities.LOW.value): (
            # then the list view's module has a key handler
            list_view_has_key_handler
        )
    }
}
