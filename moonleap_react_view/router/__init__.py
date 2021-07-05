import moonleap.resource.props as P
from moonleap import MemFun, add, extend, register_add, render_templates, tags
from moonleap.verbs import has
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import Router, RouterConfig


class StoreRouterConfigs:
    router_configs = P.tree(has, "router-config")


@register_add(RouterConfig)
def add_router_config(resource, router_configs):
    resource.router_configs.add(router_configs)


@tags(["router"])
def create_router(term, block):
    router = Router(name="UrlRouter")
    add(router, load_node_package_config(__file__))
    return router


@extend(Router)
class ExtendRouter:
    get_route_imports = MemFun(props.get_route_imports)
    get_routes = MemFun(props.get_routes)
    render = MemFun(render_templates(__file__))
