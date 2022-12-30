from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel, rule
from moonleap.blocks.verbs import has
from moonleap.render.render_mixin import get_root_resource
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule

from .resources import Route  # noqa

rules = {
    ("module", has, "route"): empty_rule(),
}


@create("routes:module")
def create_module(term):
    module = ReactModule(name="routes")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@rule("routes:module")
def created_routes_module(routes_module):
    get_root_resource().set_flags(["app/useRouter"])


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
