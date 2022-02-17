from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, add, create, create_forward, extend, rule
from moonleap.verbs import has
from titan.react_pkg.component import Component
from titan.react_pkg.nodepackage import load_node_package_config

from .props import get_context
from .resources import Router, RouterConfig  # noqa

base_tags = [("router", ["component"])]


@create("router")
def create_router(term):
    router = Router(name="UrlRouter")
    router.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(router, load_node_package_config(__file__))
    return router


@rule("react-app", has, "router")
def react_app_has_router(react_app, router):
    react_app.utils_module.use_packages(["useNextUrl", "useSearchParams"])
    return [
        create_forward(react_app, has, "routes:module"),
        create_forward("routes:module", has, router),
    ]


@extend(Component)
class ExtendComponent:
    create_router_configs = MemFun(lambda *args, **kwargs: [])
