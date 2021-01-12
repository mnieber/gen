import moonleap.props as props
import ramda as R
from leap_mn.layerconfig import LayerConfig
from moonleap import extend, output_path_from, rule, tags

from .layer_configs import get_service_layer_config
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(term.data)
    service.layer_config = LayerConfig(get_service_layer_config())
    return service


@rule("service", "configured", "layer")
def service_is_configured_in_layer(service, layer):
    layer.add_to_layer_configs(service.layer_config)


def get_output_dir(service):
    return str(output_path_from("project")(service) / service.name)


def meta():
    from leap_mn.project import Project

    @extend(Service)
    class ExtendService:
        output_dir = get_output_dir
        src_dir = props.child("has", "src-dir")
        project = props.parent(Project, "has", "service")
        layer_config = props.child("has", "layer-config")

    return [ExtendService]
