import moonleap.resource.props as P
from moonleap import (
    Forward,
    Rel,
    StoreOutputPaths,
    add,
    extend,
    kebab_to_camel,
    rule,
    tags,
    word_to_term,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has, uses
from moonleap_project.dockercompose import StoreDockerComposeConfigs
from moonleap_project.project import Project

from . import docker_compose_configs
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=kebab_to_camel(term.data))
    service.output_path = service.name + "/"

    add(service, docker_compose_configs.get(service, is_dev=True))
    add(service, docker_compose_configs.get(service, is_dev=False))

    return service


@rule(
    "service",
    has,
    "dockerfile",
    description="""
If the service has a dockerfile then we add docker options to that service.""",
)
def service_has_dockerfile(service, dockerfile):
    dockerfile.output_paths.add_source(service)
    service.docker_compose_configs.add_source(dockerfile)


@rule("service", uses, "port")
def service_uses_port(service, port):
    service.port = port.term.data


def service_has_tool_rel(service, tool):
    return Forward(
        rel=Rel(service.term, has, word_to_term(":tool")),
        subj_res=service,
        obj_res=tool,
    )


@extend(Service)
class ExtendService(
    StoreDockerComposeConfigs,
    StoreOutputPaths,
    StoreTemplateDirs,
):
    dockerfile = P.child(has, ":dockerfile")
    dockerfile_dev = P.child(has, "dev:dockerfile")
    project = P.parent(Project, has, "service")
    src_dir = P.child(has, "src-dir")
