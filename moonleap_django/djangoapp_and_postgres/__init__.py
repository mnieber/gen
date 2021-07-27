from moonleap import add, rule
from moonleap.verbs import connects
from moonleap_django.postgresservice import postgres_env_fn
from moonleap_tools.pipdependency import PipDependency, PipRequirement
from moonleap_tools.pkgdependency import PkgDependency

from . import makefile_rules


@rule("django-app", connects, "postgres:service")
def django_uses_postgres_service(django_app, postgres_service):
    add(
        django_app, PkgDependency(["postgresql-client", "psycopg2-binary"], is_dev=True)
    )
    add(django_app, PipRequirement(["psycopg2"]))
    add(django_app, PipDependency(["pgcli==2.1.1"], is_dev=True))
    add(django_app, makefile_rules.get_postgres())
    django_app.service.env_files.append(postgres_env_fn)
