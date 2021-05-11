from moonleap import add, rule, tags
from moonleap.verbs import has, uses
from moonleap_django.postgresservice import postgres_env_fn
from moonleap_project.dockerfile import create_docker_image
from moonleap_tools.pipdependency import PipDependency
from moonleap_tools.pkgdependency import PkgDependency

strapi_env_fn = "./env/strapi.env"


@tags(["strapi:docker-image"])
def strapi_docker_image_created(term, block):
    docker_image = create_docker_image(term, block)
    docker_image.name = "strapi/strapi"
    docker_image.install_command = "apt-get update && apt-get install -y"
    return docker_image


@rule("dockerfile", uses, "docker-image")
def strapi_docker_image_used(dockerfile, docker_image):
    if docker_image.name == "strapi/strapi":
        dockerfile.service.project.add_template_dir(__file__, "templates")
        dockerfile.env_vars_dev.extend(["LC_ALL=C.UTF-8", "LANG=C.UTF-8"])
        add(
            dockerfile,
            PkgDependency(["nano", "python3-pip", "postgresql-client"], is_dev=True),
        )
        add(dockerfile, PipDependency(["pgcli==2.1.1", "psycopg2-binary"], is_dev=True))


@rule("strapi:service")
def strapi_service_created(strapi_service):
    strapi_service.install_dir = "/srv/app"
    strapi_service.port = "1337"
    strapi_service.env_files.append(strapi_env_fn)


@rule("strapi:service", uses, "postgres:service")
def strapi_service_uses_postgres(strapi_service, postgres_service):
    if postgres_env_fn not in strapi_service.env_files:
        strapi_service.env_files_dev.append(postgres_env_fn)
