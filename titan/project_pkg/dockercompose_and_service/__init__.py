import moonleap.resource.props as P
from moonleap import empty_rule, extend, receives
from moonleap.verbs import has, runs
from titan.project_pkg.dockercompose.resources import DockerCompose

rules = [
    (("docker-compose", runs, "service"), empty_rule()),
    (("service", has + runs, "tool"), receives("docker_compose_configs")),
]


@extend(DockerCompose)
class ExtendDockerCompose:
    services = P.children(runs, "service")
