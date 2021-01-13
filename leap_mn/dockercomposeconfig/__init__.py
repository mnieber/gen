import moonleap.props as P
import ramda as R
from leap_mn.dockercompose import DockerCompose
from moonleap import extend

from .props import merge_configs


@extend(DockerCompose)
class ExtendDockerCompose:
    config = P.children("has", "docker-compose-config", rdcr=merge_configs)
    configs = P.children("has", "docker-compose-config")
