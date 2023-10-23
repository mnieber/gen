from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import (
    Priorities,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
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
        ),
        (has, "nav-page"): empty_rule(),
    }
}
