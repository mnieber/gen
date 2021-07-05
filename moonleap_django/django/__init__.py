from dataclasses import dataclass

from moonleap import add, rule, tags
from moonleap.verbs import runs, uses
from moonleap_tools.pipdependency import PipRequirement
from moonleap_tools.tool import Tool

from . import docker_compose_configs, layer_configs, makefile_rules, opt_paths


@dataclass
class Django(Tool):
    pass


@tags(["django"])
def create_django(term, block):
    django = Django()
    add(django, makefile_rules.get())
    add(django, layer_configs.get())
    add(django, opt_paths.static_opt_path)
    add(django, PipRequirement(["Django"], is_dev=False))
    add(django, docker_compose_configs.get(is_dev=True))
    add(django, docker_compose_configs.get(is_dev=False))
    return django


@rule("service", uses + runs, "django")
def service_has_django(service, django):
    service.port = service.port or "8000"
    add(service.project, layer_configs.get_for_project(service.name))
