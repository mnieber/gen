from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, extend, kebab_to_camel, rule
from moonleap.verbs import has
from titan.api_pkg.apiregistry import get_api_reg
from titan.react_pkg.reactapp import ReactApp

from .resources import ApiModule  # noqa

rules = {}


@create("api:module")
def create_api_module(term):
    api_module = ApiModule(name=kebab_to_camel(term.data))
    api_module.template_dir = Path(__file__).parent / "templates"
    api_module.template_context = dict(api_module=api_module, api_reg=get_api_reg())
    return api_module


@rule("api:module")
def created_api_module(api_module):
    return create_forward(":node-package", has, "graphql-api:node-pkg")


@rule("react-app", has, "api:module")
def add_api_render_tasks(react_app, api_module):
    api_module.renders(
        lambda: get_api_reg().queries,
        "queries",
        lambda query: dict(query=query),
        [Path(__file__).parent / "templates_query"],
    )

    api_module.renders(
        lambda: get_api_reg().mutations,
        "mutations",
        lambda mutation: dict(mutation=mutation),
        [Path(__file__).parent / "templates_mutation"],
    )

    api_module.renders(
        lambda: get_api_reg().get_public_items(
            lambda field_spec: "client" in field_spec.has_model
        ),
        "types",
        lambda item: dict(item=item),
        [Path(__file__).parent / "templates_type"],
    )


@extend(ReactApp)
class ExtendReactApp:
    api_module = P.child(has, "api:module")
