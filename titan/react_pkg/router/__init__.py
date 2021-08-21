import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    RenderTemplates,
    add,
    extend,
    register_add,
    rule,
    tags,
)
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


@rule("app:module", has, "router")
def app_module_has_router(app_module, router):
    app_module.react_app.utils_module.use_packages(["useNextUrl"])
    app_module.react_app.utils_module.add_template_dir(__file__, "templates_utils")


@extend(Component)
class ExtendComponent(StoreRouterConfigs):
    create_router_configs = MemFun(lambda x: None)


@extend(Router)
class ExtendRouter(RenderTemplates(__file__)):
    sections = Prop(props.Sections)
