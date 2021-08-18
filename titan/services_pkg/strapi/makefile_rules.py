from moonleap import chop0
from titan.tools_pkg.makefile import MakefileRule


def get_runserver():
    return MakefileRule(
        name="runserver",
        text=chop0(
            """
runserver:
\tdocker-entrypoint.sh strapi develop
"""
        ),
    )


def get_debugserver():
    return MakefileRule(
        name="debugserver",
        text=chop0(
            """
debugserver:
\t/usr/local/bin/node --inspect=0.0.0.0:9229 --no-lazy /usr/local/bin/strapi develop

"""
        ),
    )


def get_createdb():
    return MakefileRule(
        name="create-db",
        text=chop0(
            """
create-db:
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "CREATE USER strapi WITH CREATEDB PASSWORD 'dev';"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U strapi -c "CREATE DATABASE strapi;"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE strapi TO strapi;"
"""  # noqa
        ),
    )
