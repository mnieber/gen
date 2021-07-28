import moonleap.resource.props as P
from moonleap import MemFun, add, create_forward, extend, rule, tags
from moonleap.verbs import has, uses
from moonleap_project.service import Service, Tool
from moonleap_tools.pipdependency import PipRequirement

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
    service = P.parent(Service, has)
