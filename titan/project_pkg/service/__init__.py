import moonleap.packages.extensions.props as P
from moonleap import MemFun, create, create_forward, empty_rule, extend, kebab_to_camel
from moonleap.blocks.verbs import has, runs, uses

from . import props
from .resources import Service, Tool

render_the_service = lambda x: "render the {x.name} service"


@create("service")
def create_service(term):
    service = Service(name=kebab_to_camel(term.data))
    return service


@extend(Service)
class ExtendService:
    dockerfile = P.child(has, "dockerfile")
    docker_image = P.child(has, "docker-image")
    depends_on = P.children(uses, "service")
    is_dependent_on = MemFun(props.is_dependent_on)
    tools = P.children(uses + runs + has, "tool")
    project = P.parent("project", has)
    use_create_bundle = P.child(has, "create-bundle:makefile-command")


@extend(Tool)
class ExtendTool:
    service = P.parent("service", has + runs, required=True)


rules = {
    "service": {
        (has, "docker-image"): empty_rule(),
        (has + runs, "tool"): empty_rule(),
        (uses, "service"): empty_rule(),
        (has, "create-bundle:makefile-command"): empty_rule(),
    },
    "dockerfile": {
        (has, "docker-image"): (
            # then the service also has this docker_image
            lambda dockerfile, docker_image: create_forward(
                dockerfile.service, has, docker_image
            )
        )
    },
}
