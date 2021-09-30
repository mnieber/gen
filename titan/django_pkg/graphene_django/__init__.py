from pathlib import Path

from moonleap import MemField, add, create, create_forward, extend, rule
from moonleap.verbs import has, uses
from titan.django_pkg.module import Module
from titan.project_pkg.service import Tool
from titan.tools_pkg.pipdependency import PipRequirement

from . import django_configs
from .props import get_context


class GrapheneDjango(Tool):
    pass


base_tags = [
    ("graphene-django", ["tool"]),
]


@create("graphene-django")
def create_graphene_django(term, block):
    graphene_django = GrapheneDjango(name="graphene-django")
    graphene_django.output_path = "api"
    graphene_django.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(graphene_django, django_configs.get())
    add(graphene_django, PipRequirement(["graphene-django"]))
    return graphene_django


@rule("api:module", has, "graphql:api")
def api_module_has_graphql_api(api_module, graphql_api):
    return [
        create_forward(api_module.django_app.service, uses, ":graphene-django"),
    ]


@extend(Module)
class ExtendModule:
    has_graphql_schema = MemField(lambda: False)
