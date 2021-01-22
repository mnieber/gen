from dataclasses import dataclass

from leaptools.tool import Tool
from moonleap import add, rule, tags
from moonleap.verbs import runs, uses

from . import layer_configs, makefile_rules


@dataclass
class Django(Tool):
    pass


@rule("service", uses + runs, "django")
def service_has_django(service, django):
    service.add_tool(django)


@tags(["django"])
def create_django(term, block):
    django = Django()

    add(django, makefile_rules.get())
    add(django, layer_configs.get())

    return django
