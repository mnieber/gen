from pathlib import Path

import moonleap.resource.props as P
from moonleap import Priorities, create, extend, rule
from moonleap.verbs import has
from titan.api_pkg.typeregistry.__init__ import get_type_reg
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.djangomodule import DjangoModule


@create("api:module")
def create_api_module(term):
    api_module = DjangoModule(name="api")
    api_module.template_dir = Path(__file__).parent / "templates"
    api_module.template_context = dict(api_module=api_module)
    return api_module


@rule("django-app", has, "api:module", priority=Priorities.LOW.value)
def add_query_render_tasks(django_app, api_module):
    for query in api_module.graphql_api.queries:
        api_module.renders(
            query,
            "query",
            dict(query=query),
            [Path(__file__).parent / "templates_query"],
        )

    for mutation in api_module.graphql_api.mutations:
        api_module.renders(
            mutation,
            "mutation",
            dict(mutation=mutation),
            [Path(__file__).parent / "templates_mutation"],
        )

    for item_type in get_type_reg().item_types:
        api_module.renders(
            item_type,
            "types",
            dict(item_type=item_type),
            [Path(__file__).parent / "templates_type"],
        )


@extend(DjangoApp)
class ExtendDjangoApp:
    api_module = P.child(has, "api:module")
