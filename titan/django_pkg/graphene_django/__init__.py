import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, create_forward, extend, rule, tags
from moonleap.verbs import has, uses
from titan.django_pkg.module import Module
from titan.project_pkg.service import Tool
from titan.tools_pkg.pipdependency import PipRequirement

from . import django_configs, props


class GrapheneDjango(Tool):
    pass


@tags(["graphene-django"])
def create_graphene_django(term, block):
    graphene_django = GrapheneDjango(name="graphene-django")
    add(graphene_django, django_configs.get())
    add(graphene_django, PipRequirement(["graphene-django"]))
    return graphene_django


@rule("service", uses, "graphene-django")
def service_uses_graphene_django(service, graphene_django):
    return create_forward(service.django_app, has, "api:module")


@extend(GrapheneDjango)
class ExtendGrapheneDjango:
    render = MemFun(props.render)
    sections = Prop(props.Sections)


@extend(Module)
class ExtendModule:
    has_graphql_mutations = Prop(props.has_graphql_mutations)
    has_graphql_queries = Prop(props.has_graphql_queries)
