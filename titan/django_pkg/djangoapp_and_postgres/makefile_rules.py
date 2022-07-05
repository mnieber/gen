from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_create_db():
    return MakefileRule(
        name="create-db",
        text=chop0(
            """
create-db:
\tPGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -d postgres -U postgres -c "CREATE USER ${DJANGO_DATABASE_USER} WITH CREATEDB PASSWORD '${DJANGO_DATABASE_PASSWORD}';" || true
\tPGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -d postgres -U ${DJANGO_DATABASE_USER} -c "CREATE DATABASE ${DJANGO_DATABASE_NAME};" || true
\tPGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -d postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${DJANGO_DATABASE_NAME} TO ${DJANGO_DATABASE_USER};"
"""  # noqa: E501
        ),
    )


def get_pgcli():
    return MakefileRule(
        name="pgcli",
        text=chop0(
            """
pgcli:
\tpgcli `python manage.py sqldsn --quiet --style=uri`
"""  # noqa: E501
        ),
    )
