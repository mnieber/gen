import moonleap.resource.props as P
from moonleap import extend, register_add
from titan.project_pkg.service import Tool
from titan.react_pkg.component import Component
from titan.react_pkg.module import Module

from .resources import Flags


class StoreFlags:
    flags = P.tree("p-has", "flags")


@register_add(Flags)
def add_flags(resource, flags):
    resource.flags.add(flags)


@extend(Tool)
class ExtendTool(StoreFlags):
    pass


@extend(Component)
class ExtendComponent(StoreFlags):
    pass


@extend(Module)
class ExtendModule(StoreFlags):
    pass
