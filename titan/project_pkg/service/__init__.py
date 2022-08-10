import moonleap.resource.props as P
from moonleap import (
    MemFun,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.verbs import has, runs, uses

from . import props
from .resources import Service, Tool

render_the_service = lambda x: "render the {x.name} service"

rules = [
    (("service", has, "docker-image"), empty_rule()),
    (("service", has + runs, "tool"), empty_rule()),
    (("service", uses, "service"), empty_rule()),
]


@create("service")
def create_service(term):
    service = Service(name=kebab_to_camel(term.data))
    return service


@rule("dockerfile", has, "docker-image")
def dockerfile_use_docker_image(dockerfile, docker_image):
    return create_forward(dockerfile.service, has, docker_image)


@rule("service", uses + has + runs, "tool")
def service_runs_tool(service, tool):
    service.renders(
        tool,
        "",
        tool.template_context,
        [tool.template_dir],
    )


@rule("project", has, "service")
def project_has_service(project, service):
    project.renders(
        service,
        service.name,
        dict(service=service),
        [],
    )


@extend(Service)
class ExtendService:
    dockerfile = P.child(has, "dockerfile")
    docker_image = P.child(has, "docker-image")
    depends_on = P.children(uses, "service")
    is_dependent_on = MemFun(props.is_dependent_on)
    tools = P.children(uses + runs + has, "tool")
    project = P.parent("project", has)


@extend(Tool)
class ExtendTool:
    service = P.parent("service", has + runs, required=True)
