from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, extend, get_root_resource, rule
from moonleap.blocks.verbs import has
from titan.api_pkg.apiregistry import get_api_reg
from titan.api_pkg.apiregistry.get_public_type_specs import get_public_type_specs
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import create_react_module
from titan.types_pkg.typeregistry import get_type_reg

from .resources import ApiModule  # noqa

rules = {}


@create("api:module")
def create_api_module(term):
    api_module = create_react_module(
        ApiModule, term, Path(__file__).parent / "templates"
    )
    api_module.render_context = lambda api_module: dict(
        module=api_module, api_reg=get_api_reg()
    )
    return api_module


@rule("react-app", has, "api:module")
def react_app_uses_graphql(react_app, api_module):
    use_graphql = False
    for endpoint in get_api_reg().get_queries(
        module_name="api"
    ) + get_api_reg().get_mutations(module_name="api"):
        if not endpoint.api_spec.is_stub:
            use_graphql = True
    if use_graphql:
        return create_forward(":react-app", has, ":graphql")


@rule("react-app", has, ":graphql")
def react_app_uses_graphql_node_pkg(react_app, graphql):
    get_root_resource().set_flags(["app/useGraphql"])


@rule("react-app", has, "api:module")
def add_api_render_tasks(react_app, api_module):
    type_reg = get_type_reg()

    api_module.renders(
        lambda: [
            x
            for x in sorted(
                get_api_reg().get_queries(module_name="api"), key=lambda x: x.name
            )
            if x.api_spec.has_endpoint
        ],
        "queries",
        lambda query: dict(query=query),
        [Path(__file__).parent / "templates_query"],
    )

    api_module.renders(
        lambda: [
            x
            for x in sorted(
                get_api_reg().get_mutations(module_name="api"), key=lambda x: x.name
            )
            if x.api_spec.has_endpoint
        ],
        "mutations",
        lambda mutation: dict(mutation=mutation, api_reg=get_api_reg()),
        [Path(__file__).parent / "templates_mutation"],
    )

    api_module.renders(
        lambda: [get_api_reg()],
        "endpoints",
        lambda api_reg: dict(),
        [Path(__file__).parent / "templates_endpoints"],
    )

    api_module.renders(
        lambda: get_public_type_specs(
            get_api_reg(),
            include_stubs=True,
            predicate=lambda field_spec: field_spec.has_model,
        ),
        "types",
        lambda type_spec: dict(
            type_spec=type_spec,
            form_type_spec=type_reg.get(type_spec.type_name + "Form", None),
        ),
        [Path(__file__).parent / "templates_type"],
    )


@extend(ReactApp)
class ExtendReactApp:
    api_module = P.child(has, "api:module")
