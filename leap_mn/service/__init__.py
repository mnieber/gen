from dataclasses import dataclass
from pathlib import Path

import moonleap.props as props
import ramda as R
from leap_mn.layerconfig import LayerConfig
from moonleap import Resource, rule, tags
from moonleap.config import config, extend, output_path_from
from moonleap.slctrs import Selector

from .layer_configs import get_service_layer_config


@dataclass
class Service(Resource):
    name: str


package_names_rdcr = R.reduce(
    lambda acc, x: R.concat(acc, R.map(R.prop("package_names"))(x)), []
)


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
