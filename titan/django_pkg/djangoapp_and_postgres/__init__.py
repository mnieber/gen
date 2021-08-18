from moonleap import add, create_forward, rule
from moonleap.verbs import connects, uses
from titan.services_pkg.postgresservice import postgres_env_fn
from titan.tools_pkg.pipdependency import PipDependency, PipRequirement
from titan.tools_pkg.pkgdependency import PkgDependency

from . import makefile_rules


@rule("django-app", connects, "postgres:service")
def django_uses_postgres_service(django_app, postgres_service):
    add(django_app, PkgDependency(["postgresql-client"], is_dev=True))
    add(django_app, PipRequirement(["psycopg2"]))
    add(django_app, PipDependency(["pgcli==2.1.1"], is_dev=True))
    add(django_app, makefile_rules.get_create_db())
    add(django_app, makefile_rules.get_pgcli())
    django_app.service.env_files.append(postgres_env_fn)

    return create_forward(django_app.service, uses, "postgres:service")
