import moonleap.resource.props as P
from moonleap import add_source, empty_rule, extend, rule
from moonleap.verbs import has, runs
from titan.project_pkg.dockercompose.resources import DockerCompose


@rule("service", has + runs, "tool")
def service_has_tool(service, tool):
    add_source(
        [service, "docker_compose_configs"],
        tool,
        "The :service receives docker compose configs from a :tool",
    )


rules = [(("docker-compose", runs, "service"), empty_rule())]


@extend(DockerCompose)
class ExtendDockerCompose:
    services = P.children(runs, "service")
