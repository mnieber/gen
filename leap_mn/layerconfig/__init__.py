from moonleap.config import reduce
from moonleap.resource import Resource


class LayerConfig(Resource):
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def describe(self):
        return dict(name=self.name)


@reduce(parent_resource="leap_mn.Layer", resource=LayerConfig)
def add_config(layer, layer_config):
    if layer_config.is_created_in_block_that_mentions(layer):
        layer.sections.append(layer_config)
