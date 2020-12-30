from moonleap.config import reduce
from moonleap.resource import Resource


class LayerGroup(Resource):
    def __init__(self, name):
        self.name = name
        self.layer_by_name = {}

    def describe(self):
        return {
            str(self): dict(
                name=self.name,
                layers=[x.describe() for x in self.layer_by_name.values()],
            )
        }


def create(term, line, block):
    return [LayerGroup(name=term.data)]


@reduce(LayerGroup, resource_id="leap_mn.layer")
def add_layer(layer_group, layer):
    if layer_group.is_mentioned_in_same_line(layer) and not layer.is_root:
        layer.path = f"{layer_group.name}.{layer.name}.yaml"
        layer_group.layer_by_name.setdefault(layer.name, layer)
        layer.drop_from_block()


is_ittable = True


tags = ["layer-group"]
