import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, extend, register_add, render_templates, tags
from moonleap.verbs import has
from titan.react_pkg.component import Component
from titan.react_pkg.nodepackage import load_node_package_config

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


@extend(Component)
class ExtendComponent(StoreRouterConfigs):
    create_router_configs = MemFun(lambda x: None)


@extend(Router)
class ExtendRouter:
    p_section_route_imports = Prop(props.p_section_route_imports)
    p_section_routes = Prop(props.p_section_routes)
    render = MemFun(render_templates(__file__))
