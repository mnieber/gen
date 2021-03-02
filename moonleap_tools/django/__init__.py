from dataclasses import dataclass

from moonleap import add, extend, rule, tags
from moonleap.verbs import has, runs, uses
from moonleap_tools.tool import Tool

from . import layer_configs, makefile_rules


@dataclass
class Django(Tool):
    pass


@rule("service", uses + runs, "django")
def service_has_django(service, django):
    add(service.project, layer_configs.get_for_project(service.name))
    service.add_tool(django)


@tags(["django"])
def create_django(term, block):
    django = Django()
    add(django, makefile_rules.get())
    add(django, layer_configs.get())
    return django
