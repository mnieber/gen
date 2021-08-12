from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_postgres():
    return MakefileRule(
        chop0(
            """
create-db:
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "CREATE USER django WITH CREATEDB PASSWORD 'dev';"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U django -c "CREATE DATABASE django;"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE django TO django;"

pgcli:
\tpgcli `./manage.py sqldsn --quiet --style=uri`
"""  # noqa
        )
    )
