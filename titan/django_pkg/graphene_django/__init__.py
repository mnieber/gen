from moonleap import MemField, create, create_forward, extend, rule
from moonleap.verbs import has, uses
from titan.django_pkg.djangomodule import DjangoModule
from titan.project_pkg.service import Tool


class GrapheneDjango(Tool):
    pass


base_tags = [
    ("graphene-django", ["tool"]),
]


@create("graphene-django")
def create_graphql_auth(term):
    return Tool(name="graphene_django")


@rule("api:module", has, "graphql:api")
def api_module_has_graphql_api(api_module, graphql_api):
    return [
        create_forward(api_module.django_app.service, uses, ":graphene-django"),
    ]


@extend(DjangoModule)
class ExtendModule:
    has_graphql_schema = MemField(lambda: False)
