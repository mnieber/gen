from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import Priorities, create, create_forward, extend, kebab_to_camel, rule
from moonleap.blocks.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule, create_react_module

from .resources import NavPage, Route  # noqa


@create("routes:module")
def create_routes_module(term):
    return create_react_module(ReactModule, term, Path(__file__).parent / "templates")


@rule("routes:module")
def created_routes_module(routes_module):
    routes_module.react_app.set_flags(["app/useRouter"])


@create("route")
def create_route(term):
    route = Route(name=kebab_to_camel(term.data), path=term.data)
    return route


@create("nav-page")
def create_nav_page(term):
    nav_page = NavPage()
    return nav_page


@rule("module", has, "nav-page", priority=Priorities.LOW.value)
def module_has_nav_page(module, nav_page):
    frames_module = module.react_app.frames_module
    if frames_module:
        frames_module.renders(
            [nav_page],
            f"pages",
            lambda nav_page: dict(nav_page=nav_page),
            [Path(__file__).parent / "templates_pages"],
        )


@extend(ReactModule)
class ExtendModule:
    routes = P.children(has, "route")


@extend(NavPage)
class ExtendNavPage:
    module = P.parent("module", has)


@extend(ReactApp)
class ExtendReactApp:
    routes_module = P.child(has, "routes:module")


rules = {
    "module": {
        (has, "route"): (
            # then the module has a nav-page
            lambda module, route: create_forward(module, has, f"{module.name}:nav-page")
        )
    }
}
