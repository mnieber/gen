
import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, extend
from moonleap.blocks.verbs import has
from titan.api_pkg.apiregistry import get_api_reg
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import create_react_module

from .resources import ApiModule  # noqa


@create("api:module")
def create_api_module(term):
    api_module = create_react_module(ApiModule, term)
    api_module.render_context = lambda api_module: dict(
        module=api_module, api_reg=get_api_reg()
    )
    return api_module


def react_app_maybe_uses_graphql(react_app, api_module):
    use_graphql = False
    for endpoint in get_api_reg().get_queries(
        module_name="api"
    ) + get_api_reg().get_mutations(module_name="api"):
        if not endpoint.api_spec.is_stub:
            use_graphql = True
    if use_graphql:
        return create_forward(react_app, has, ":graphql")


@extend(ReactApp)
class ExtendReactApp:
    api_module = P.child(has, "api:module")


rules = {
    "react-app": {
        (has, "api:module"): (
            # Maybe add the relation that react_app uses graphql
            react_app_maybe_uses_graphql
        ),
        (has, ":graphql"): (
            # set the useGraphql flag
            lambda react_app, graphql: react_app.set_flags(["app/useGraphql"])
        ),
    },
}
