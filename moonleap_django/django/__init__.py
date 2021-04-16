from dataclasses import dataclass

from moonleap import add, rule, tags
from moonleap.verbs import runs, uses
from moonleap_project.service import service_has_tool_rel
from moonleap_tools.pipdependency import PipRequirement
from moonleap_tools.tool import Tool

from . import layer_configs, makefile_rules


@dataclass
class Django(Tool):
    pass


@tags(["django"])
def create_django(term, block):
    django = Django()
    add(django, makefile_rules.get())
    add(django, layer_configs.get())
    add(django, PipRequirement(["Django"], is_dev=False))
    return django


@rule("service", uses + runs, "django")
def service_has_django(service, django):
    add(service.project, layer_configs.get_for_project(service.name))
    return service_has_tool_rel(service, django)
