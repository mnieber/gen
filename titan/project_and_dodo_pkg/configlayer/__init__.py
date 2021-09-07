from moonleap import add
from moonleap.builder.rule import rule

from . import dodo_layer_configs


@rule("config:layer")
def config_layer_created(layer):
    add(layer, dodo_layer_configs.get_root_config())
