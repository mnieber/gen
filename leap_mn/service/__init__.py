import moonleap.props as P
import ramda as R
from leap_mn.layer import LayerConfig, StoreLayerConfigs
from leap_mn.project import Project
from moonleap import extend, output_path_from, rule, tags

from .layer_configs import get_service_layer_config
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(term.data)
    service.add_to_layer_configs(LayerConfig(get_service_layer_config()))
    return service


def get_output_dir(service):
    return str(output_path_from("project")(service) / service.name)


@extend(Service)
class ExtendService(StoreLayerConfigs):
    output_dir = get_output_dir
    src_dir = P.child("has", "src-dir")
    project = P.parent(Project, "has", "service")
