import moonleap.resource.props as P
from moonleap import (MemFun, add, extend, register_add, render_templates,
                      rule, tags)
from moonleap.verbs import has
from moonleap_project.service import Service, service_has_tool_rel
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config
from moonleap_react_module.appmodule import AppModule
from moonleap_tools.tool import Tool

from . import props
from .resources import Router, RouterConfig


@tags(["router"])
def create_router(term, block):
    router = Router(name="UrlRouter")
    add(router, load_node_package_config(__file__))
    return router


@rule("app:module", has, "router")
def service_has_router(app_module, router):
    router.output_path = app_module.output_path
    return service_has_tool_rel(app_module.service, router)


@extend(Router)
class ExtendRouter:
    module = P.parent(Module, has, "router")
    get_route_imports = MemFun(props.get_route_imports)
    get_routes = MemFun(props.get_routes)
    render = MemFun(render_templates(__file__))


@rule("service", has, "tool")
def service_has_tool(service, tool):
    service.router_configs.add_source(tool)


class StoreRouterConfigs:
    router_configs = P.tree("has", "router-config")


@register_add(RouterConfig)
def add_router_config(resource, router_config):
    resource.router_configs.add(router_config)


@extend(Tool)
class ExtendTool(StoreRouterConfigs):
    pass


@extend(Service)
class ExtendService(StoreRouterConfigs):
    pass


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")
