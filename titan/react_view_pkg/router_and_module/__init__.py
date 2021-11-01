import moonleap.resource.props as P
from moonleap import extend, register_add
from moonleap.verbs import has
from titan.react_pkg.module import Module

from .resources import RouteTable


@register_add(RouteTable)
def add_route_table(resource, route_table):
    resource.route_tables.add(route_table)


@extend(Module)
class ExtendModule:
    route_tables = P.tree("route_tables")
