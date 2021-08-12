from moonleap import add, rule, tags
from titan.project_pkg.service.__init__ import create_service

from . import docker_compose_configs

postgres_env_fn = "./env/postgres.env"


@tags(["postgres:service"])
def create_postgres_service(term, block):
    postgres_service = create_service(term, block)
    postgres_service.env_files.append(postgres_env_fn)
    add(postgres_service, docker_compose_configs.get(is_dev=True))
    add(postgres_service, docker_compose_configs.get(is_dev=False))
    return postgres_service


@rule("postgres:service")
def postgres_service_created(postgres_service):
    postgres_service.port = postgres_service.port or "5432"
    postgres_service.project.add_template_dir(__file__, "templates")
