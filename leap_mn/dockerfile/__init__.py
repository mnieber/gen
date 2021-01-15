import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.outputpath import StoreOutputPaths
from leap_mn.service import Service
from moonleap import extend, render_templates, rule, tags

from . import layer_configs as LC
from .resources import Dockerfile


@tags(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile(is_dev=term.data == "dev")
    return docker_file


@rule("dockerfile", "use", "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    dockerfile.image_name = docker_image.term.data


@rule(
    "service",
    "has",
    "dockerfile",
    description="""
If the service has a dockerfile then we add docker options to that service.""",
)
def service_has_dockerfile(service, dockerfile):
    service.layer_configs.add(LayerConfig(lambda: LC.get_docker_options(service)))
    dockerfile.output_paths.add_source(service)


def get_template_filename(dockerfile):
    return "templates/Dockerfile" + (".dev" if dockerfile.is_dev else "")


@extend(Dockerfile)
class ExtendDockerfile(StoreOutputPaths):
    service = P.parent(Service, "has", "dockerfile")
    render = render_templates(__file__, get_template_filename)


@extend(Service)
class ExtendService:
    dockerfile = P.child("has", ":dockerfile")
    dockerfile_dev = P.child("has", "dev:dockerfile")
