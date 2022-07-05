from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_run_server():
    return MakefileRule(
        name="run-server",
        text=chop0(
            """
run-server:
\tdocker-entrypoint.sh strapi develop
"""
        ),
    )


def get_debug_server():
    return MakefileRule(
        name="debug-server",
        text=chop0(
            """
debug-server:
\t/usr/local/bin/node --inspect=0.0.0.0:9229 --no-lazy /usr/local/bin/strapi develop
"""
        ),
    )


def get_createdb():
    return MakefileRule(
        name="create-db",
        text=chop0(
            """
\tPGPASSWORD=${POSTGRES_PASSWORD} psql -h postgres -d postgres -U postgres -c "CREATE USER ${DJANGO_DATABASE_USER} WITH CREATEDB PASSWORD '${DJANGO_DATABASE_PASSWORD}';" || true
\tPGPASSWORD=${POSTGRES_PASSWORD} psql -h postgres -d postgres -U ${DJANGO_DATABASE_USER} -c "CREATE DATABASE ${DJANGO_DATABASE_NAME};" || true
\tPGPASSWORD=${POSTGRES_PASSWORD} psql -h postgres -d postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${DJANGO_DATABASE_NAME} TO ${DJANGO_DATABASE_USER};"
"""  # noqa: E501
        ),
    )
