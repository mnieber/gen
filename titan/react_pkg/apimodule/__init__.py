from pathlib import Path

import moonleap.resource.props as P
from moonleap import Priorities, create, empty_rule, extend, kebab_to_camel, rule
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactApp

from .resources import ApiModule  # noqa

rules = [(("api:module", has, "graphql:api"), empty_rule())]


@create("api:module")
def create_api_module(term):
    api_module = ApiModule(name=kebab_to_camel(term.data))
    api_module.template_dir = Path(__file__).parent / "templates"
    api_module.template_context = dict(api_module=api_module)
    return api_module


@rule("react-app", has, "module")
def react_app_has_module(react_app, module):
    react_app.get_module("utils").use_packages(["graphqlClient"])


@rule("react-app", has, "api:module", priority=Priorities.LOW.value)
def add_api_render_tasks(react_app, api_module):
    for query in api_module.graphql_api.queries:
        api_module.renders(
            query,
            "queries",
            dict(query=query),
            [Path(__file__).parent / "templates_query"],
        )

    for mutation in api_module.graphql_api.mutations:
        api_module.renders(
            mutation,
            "mutations",
            dict(mutation=mutation),
            [Path(__file__).parent / "templates_mutation"],
        )


@extend(ApiModule)
class ExtendApiModule:
    graphql_api = P.child(has, "graphql:api")


@extend(ReactApp)
class ExtendReactApp:
    api_module = P.child(has, "api:module")
