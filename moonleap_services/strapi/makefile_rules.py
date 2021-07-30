from moonleap import chop0
from moonleap_tools.makefile import MakefileRule


def get():
    return MakefileRule(
        chop0(
            """
runserver:
\tdocker-entrypoint.sh strapi develop

debugserver:
\t/usr/local/bin/node --inspect=0.0.0.0:9229 --no-lazy /usr/local/bin/strapi develop

"""
        )
    )


def get_postgres():
    return MakefileRule(
        chop0(
            """
create-db:
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "CREATE USER strapi WITH CREATEDB PASSWORD 'dev';"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U strapi -c "CREATE DATABASE strapi;"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE strapi TO strapi;"
"""  # noqa
        )
    )
