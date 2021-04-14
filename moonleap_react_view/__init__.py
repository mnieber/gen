import os

from moonleap import install
from moonleap.render.template_env import add_filter
from moonleap.utils.case import title0
from moonleap.utils.inflect import plural

from . import (
    formsmodule,
    formview,
    frame,
    itemview,
    listview,
    panel,
    router,
    router_and_module,
    router_and_service,
    view,
    view_and_module,
)


def install_all():
    install(formsmodule)
    install(formview)
    install(frame)
    install(itemview)
    install(listview)
    install(panel)
    install(router)
    install(router_and_module)
    install(router_and_service)
    install(view)
    install(view_and_module)


add_filter("plural", lambda x: plural(x))
add_filter("title0", title0)
add_filter("expand_vars", lambda x: os.path.expandvars(x))
add_filter("dbg", lambda x: __import__("pudb").set_trace())
