import moonleap.resource.props as P
from moonleap import add, create_forward, extend, rule, tags
from moonleap.verbs import connects, has, runs, uses
from moonleap_django.postgresservice import postgres_env_fn
from moonleap_project.service import Service
from moonleap_tools.pipdependency import PipDependency, PipRequirement
from moonleap_tools.pkgdependency import PkgDependency

from . import docker_compose_configs, layer_configs, makefile_rules, opt_paths
from .resources import Django


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
    return create_forward(service, has, ":makefile")


@rule("django", connects, "postgres:service")
def django_uses_postgres_service(django, postgres_service):
    add(django, PkgDependency(["postgresql-client", "psycopg2-binary"], is_dev=True))
    add(django, PipRequirement(["psycopg2"]))
    add(django, PipDependency(["pgcli==2.1.1"], is_dev=True))
    add(django, makefile_rules.get_postgres())
    django.service.env_files.append(postgres_env_fn)


@extend(Django)
class ExtendDjango:
    service = P.parent(Service, uses + runs)
