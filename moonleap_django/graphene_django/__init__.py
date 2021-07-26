from moonleap import add, extend, rule, tags
from moonleap.verbs import uses
from moonleap_project.service import Tool
from moonleap_tools.pipdependency import PipRequirement

from . import django_configs


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
    pass


@extend(GrapheneDjango)
class ExtendGrapheneDjango:
    pass
