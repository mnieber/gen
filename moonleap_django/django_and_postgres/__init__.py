from moonleap import add, rule
from moonleap.verbs import connects
from moonleap_django.postgresservice import postgres_env_fn
from moonleap_tools.pipdependency import PipDependency, PipRequirement
from moonleap_tools.pkgdependency import PkgDependency

from . import makefile_rules


@rule("django", connects, "postgres:service")
def django_uses_postgres_service(django, postgres_service):
    add(django, PkgDependency(["postgresql-client", "psycopg2-binary"], is_dev=True))
    add(django, PipRequirement(["psycopg2"]))
    add(django, PipDependency(["pgcli==2.1.1"], is_dev=True))
    add(django, makefile_rules.get_postgres())
    django.service.env_files.append(postgres_env_fn)
