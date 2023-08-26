from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend, kebab_to_camel, rule
from moonleap.blocks.verbs import has
from moonleap.render.render_mixin import get_root_resource
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule, create_react_module

from .resources import Route  # noqa

rules = {
    ("module", has, "route"): empty_rule(),
}


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


@extend(ReactModule)
class ExtendModule:
    routes = P.children(has, "route")


@extend(ReactApp)
class ExtendReactApp:
    routes_module = P.child(has, "routes:module")
