from moonleap import add, rule, tags
from moonleap.verbs import uses
from moonleap_project.dockerfile import create_docker_image
from moonleap_tools.pipdependency import PipDependency
from moonleap_tools.pkgdependency import PkgDependency

from . import makefile_rules

strapi_env_fn = "./env/strapi.env"


custom_steos_pre_dev = """ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
"""


@tags(["strapi:docker-image"])
def strapi_docker_image_created(term, block):
    docker_image = create_docker_image(term, block)
    docker_image.name = "strapi/strapi"
    docker_image.install_command = "apt-get update && apt-get install -y"
    add(docker_image, makefile_rules.get())
    return docker_image


@rule("dockerfile", uses, "docker-image")
def strapi_docker_image_used(dockerfile, docker_image):
    if docker_image.name == "strapi/strapi":
        dockerfile.custom_steps_pre_dev += custom_steos_pre_dev
        add(
            dockerfile,
            PkgDependency(["nano", "python3-pip", "postgresql-client"], is_dev=True),
        )
        add(dockerfile, PipDependency(["pgcli==2.1.1", "psycopg2-binary"], is_dev=True))


@rule("service", uses, "strapi")
def service_uses_strapi(service, strapi):
    service.install_dir = "/srv/app"
    service.port = "1337"
    service.env_files.append(strapi_env_fn)
    service.project.add_template_dir(__file__, "templates")
