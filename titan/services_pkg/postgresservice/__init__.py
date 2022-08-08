from pathlib import Path

from moonleap import add, create, rule
from titan.project_pkg.service import create_service

from . import docker_compose_configs

postgres_env_fn = "./env/postgres.env"


@create("postgres:service")
def create_postgres_service(term):
    postgres_service = create_service(term)
    postgres_service.env_files.append(postgres_env_fn)
    add(postgres_service, docker_compose_configs.get("dev"))
    add(postgres_service, docker_compose_configs.get("prod"))
    return postgres_service


@rule("postgres:service")
def postgres_service_created(postgres_service):
    postgres_service.port = postgres_service.port or "5432"
    postgres_service.project.add_template_dir(Path(__file__).parent / "templates")
