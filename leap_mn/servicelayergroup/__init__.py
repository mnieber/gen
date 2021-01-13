import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.layergroup import LayerGroup, get_layer_config
from leap_mn.service import Service
from moonleap import extend, rule, tags

from .layer_configs import get_dial_config


@tags(["service:layer-group"])
def create_service_layer_group(term, block):
    layer_group = LayerGroup(name="server")
    layer_group.layer_config = LayerConfig(
        lambda: dict(
            DIAL=get_dial_config(layer_group),
            LAYER_GROUPS=get_layer_config(layer_group),
        ),
    )
    return layer_group


@rule("service", "configured", "layer")
def service_is_configured_in_layer(service, layer):
    layer.add_to_layer_configs(service.layer_config)


@extend(Service)
class ExtendService:
    layer = P.child("configured", "layer")
