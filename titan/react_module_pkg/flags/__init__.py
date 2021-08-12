import moonleap.resource.props as P
from moonleap import extend, register_add
from moonleap.verbs import has
from titan.project_pkg.service import Tool

from .resources import Flags  # noqa


class StoreFlags:
    flags = P.tree(has, "flags")


@register_add(Flags)
def add_flags(resource, flags):
    resource.flags.add(flags)


@extend(Tool)
class ExtendTool(StoreFlags):
    pass
