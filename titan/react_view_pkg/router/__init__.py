from pathlib import Path

from moonleap import MemField, create, create_forward, extend, register_add, rule
from moonleap.verbs import has
from titan.react_pkg.reactmodule import ReactModule

from .resources import Router, RouteTable  # noqa

base_tags = [("router", ["component"])]


@create("router")
def create_router(term):
    router = Router(name="UrlRouter")
    router.template_dir = Path(__file__).parent / "templates"
    return router


@rule("react-app", has, "router")
def react_app_has_router(react_app, router):
    react_app.get_module("utils").use_packages(["useNextUrl", "useSearchParams"])
    return [
        create_forward(react_app, has, "routes:module"),
        create_forward("routes:module", has, router),
    ]


@register_add(RouteTable)
def add_route_table(resource, route_table):
    resource.route_tables.append(route_table)


@extend(ReactModule)
class ExtendModule:
    route_tables = MemField(lambda: list())
