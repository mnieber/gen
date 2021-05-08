import os

from moonleap import DocMeta, install
from moonleap.parser.term import term_to_word, verb_to_word
from moonleap.render.template_env import add_filter
from moonleap.utils.case import lower0, upper0
from moonleap.utils.inflect import plural

from . import (
    formsmodule,
    formview,
    frame,
    frame_and_panel,
    panel,
    router,
    router_and_module,
    view,
)


def install_all():
    install(formsmodule)
    install(formview)
    install(frame)
    install(frame_and_panel)
    install(panel)
    install(router)
    install(router_and_module)
    install(view)


add_filter("plural", lambda x: plural(x))
add_filter("upper0", upper0)
add_filter("term_to_word", lambda x: x if x is None else term_to_word(x))
add_filter("verb_to_word", verb_to_word)
add_filter("lower0", lower0)
add_filter("expand_vars", lambda x: os.path.expandvars(x))
add_filter("dbg", lambda x: __import__("pudb").set_trace())
add_filter(
    "doc_meta",
    lambda x: x.__class__.doc_meta if hasattr(x.__class__, "doc_meta") else DocMeta(),
)
