from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, add, create, extend, register_add, rule
from moonleap.verbs import has
from titan.react_pkg.component import Component
from titan.react_pkg.nodepackage import load_node_package_config

from .props import get_context
from .resources import Router, RouterConfig


class StoreRouterConfigs:
    router_configs = P.tree("p-has", "router-config")


@register_add(RouterConfig)
def add_router_config(resource, router_configs):
    resource.router_configs.add(router_configs)


base_tags = [("router", ["component"])]


@create("router")
def create_router(term, block):
    router = Router(name="UrlRouter")
    router.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(router, load_node_package_config(__file__))
    return router


@rule("app:module", has, "router")
def app_module_has_router(app_module, router):
    app_module.react_app.utils_module.use_packages(["useNextUrl", "useSearchParams"])
    app_module.react_app.utils_module.add_template_dir(
        Path(__file__).parent / "templates_utils"
    )


@extend(Component)
class ExtendComponent(StoreRouterConfigs):
    create_router_configs = MemFun(lambda x: [])
