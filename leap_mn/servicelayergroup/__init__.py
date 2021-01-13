import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.layergroup import LayerGroup, create_layer_group
from leap_mn.service import Service
from moonleap import Term, extend, rule, tags

from . import layer_configs as LC


@tags(["service:layer-group"])
def create_service_layer_group(term, block):
    layer_group = create_layer_group(Term("server", "layer-group"), block)
    layer_group.add_to_layer_configs(
        LayerConfig(lambda: LC.get_dial_config(layer_group))
    )
    return layer_group


@rule("service", "configured", "layer")
def service_is_configured_in_layer(service, layer):
    layer.add_to_layer_config_sources(service)


@extend(Service)
class ExtendService:
    layer = P.child("configured", "layer")
