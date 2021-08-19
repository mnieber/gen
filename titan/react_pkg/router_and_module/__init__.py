import moonleap.resource.props as P
from moonleap import Prop, extend, register_add, rule
from moonleap.verbs import has
from titan.react_module_pkg.appmodule import AppModule
from titan.react_pkg.module import Module

from . import props
from .resources import RouteTable


@rule("app:module", has, "router")
def app_module_has_router(app_module, router):
    app_module.react_app.utils_module.use_packages(["RouteTable"])
    app_module.add_template_dir(__file__, "templates_app")


@register_add(RouteTable)
def add_route_table(resource, route_table):
    resource.route_tables.add(route_table)


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")
    sections = Prop(props.Sections)


@extend(Module)
class ExtendModule:
    route_tables = P.tree(has, "route-table")
