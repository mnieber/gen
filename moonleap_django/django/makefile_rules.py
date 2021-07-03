from moonleap import chop0
from moonleap_tools.makefile import MakefileRule


def get():
    return MakefileRule(
        chop0(
            """
runserver:
\tpython manage.py runserver 0.0.0.0:8000 --nostatic

create-db:
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "CREATE USER django WITH CREATEDB PASSWORD 'dev';"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U django -c "CREATE DATABASE django;"
\tenv PGPASSWORD=dev psql -h postgres -d postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE django TO django;"

"""
        )
    )
