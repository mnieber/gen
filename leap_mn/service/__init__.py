import moonleap.props as P
import ramda as R
from leap_mn.dockercompose import DockerComposeConfig, StoreDockerComposeConfigs
from leap_mn.layer import LayerConfig, StoreLayerConfigs
from leap_mn.project import Project
from moonleap import extend, output_path_from, rule, tags

from . import docker_compose_configs as DCC
from . import layer_configs as LC
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=term.data)
    service.add_to_layer_configs(LayerConfig(body=LC.get_service_options()))
    service.add_to_docker_compose_configs(
        DockerComposeConfig(
            lambda docker_compose_config: DCC.get_service_options(
                service, docker_compose_config
            )
        )
    )
    service.add_to_docker_compose_configs(
        DockerComposeConfig(
            lambda docker_compose_config: DCC.get_service_options(
                service, docker_compose_config
            ),
            is_dev=True,
        )
    )
    return service


def get_output_dir(service):
    return str(output_path_from("project")(service) / service.name)


@extend(Service)
class ExtendService(StoreLayerConfigs, StoreDockerComposeConfigs):
    output_dir = get_output_dir
    src_dir = P.child("has", "src-dir")
    project = P.parent(Project, "has", "service")
