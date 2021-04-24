from moonleap import add, tags
from moonleap_project.service.resources import Service

from . import docker_compose_configs


@tags(["postgres:service"])
def create_postgres_service(term, block):
    service = Service(name="db", use_default_config=False)
    add(service, docker_compose_configs.get(is_dev=True))
    add(service, docker_compose_configs.get(is_dev=False))
    service.add_template_dir(__file__, "templates")
    return service
