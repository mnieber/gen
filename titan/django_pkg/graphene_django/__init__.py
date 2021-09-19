from moonleap import MemField, MemFun, Prop, add, create, create_forward, extend, rule
from moonleap.verbs import has, uses
from titan.django_pkg.module import Module
from titan.project_pkg.service import Tool
from titan.tools_pkg.pipdependency import PipRequirement

from . import django_configs, props


class GrapheneDjango(Tool):
    pass


@create(["graphene-django"])
def create_graphene_django(term, block):
    graphene_django = GrapheneDjango(name="graphene-django")
    graphene_django.output_path = "api"
    add(graphene_django, django_configs.get())
    add(graphene_django, PipRequirement(["graphene-django"]))
    return graphene_django


@rule("api:module", has, "graphql:api")
def api_module_has_graphql_api(api_module, graphql_api):
    return [
        create_forward(api_module.django_app.service, uses, ":graphene-django"),
    ]


@extend(GrapheneDjango)
class ExtendGrapheneDjango:
    render = MemFun(props.render)
    sections = Prop(props.Sections)


@extend(Module)
class ExtendModule:
    has_graphql_schema = MemField(lambda: False)
