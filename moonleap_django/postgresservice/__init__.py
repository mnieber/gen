from moonleap import add, rule
from moonleap.verbs import uses

from . import docker_compose_configs

postgres_env_fn = "./env/postgres.env"


@rule("service", uses, "docker-image")
def service_uses_postgres_docker_image(service, docker_image):
    if docker_image.name.startswith("postgres:"):
        _postgres_docker_image_used(docker_image, service)


@rule("dockerfile", uses, "docker-image")
def dockerfile_uses_postgres_docker_image(dockerfile, docker_image):
    if docker_image.name.startswith("postgres:"):
        _postgres_docker_image_used(docker_image, dockerfile.service)


@rule("service", uses, "postgres:service")
def service_uses_postgres(service, postgres_service):
    if postgres_env_fn not in service.env_files:
        service.env_files_dev.append(postgres_env_fn)


def _postgres_docker_image_used(docker_image, service):
    service.port = "5432"
    service.env_files.append(postgres_env_fn)
    add(service, docker_compose_configs.get(is_dev=True))
    add(service, docker_compose_configs.get(is_dev=False))
    service.project.add_template_dir(__file__, "templates")
