from dataclasses import dataclass

from moonleap import add, rule, tags
from moonleap.verbs import connects, runs, uses
from moonleap_tools.pipdependency import PipDependency, PipRequirement
from moonleap_tools.pkgdependency import PkgDependency
from moonleap_tools.tool import Tool

from . import docker_compose_configs, layer_configs, makefile_rules, opt_paths


@dataclass
class Django(Tool):
    pass


@tags(["django"])
def create_django(term, block):
    django = Django(name="django")
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


@rule("django", connects, "postgres:service")
def django_uses_postgres_service(django, postgres_service):
    add(django, PkgDependency(["postgresql-client", "psycopg2-binary"], is_dev=True))
    add(django, PipRequirement(["psycopg2"]))
    add(django, PipDependency(["pgcli==2.1.1"], is_dev=True))
    add(django, makefile_rules.get_postgres())
