from moonleap.config import reduce
from moonleap.resource import Resource


class Layer(Resource):
    def __init__(self, name):
        self.name = name
        self.is_root = name == "root"
        self.path = f"config.yaml" if self.is_root else f"{name}.yaml"
        self.layer_groups = []
        self.sections = []
        self.src_dir = None

    def describe(self):
        return {
            str(self): dict(
                name=self.name,
                path=self.path,
                layer_groups=[x.name for x in self.layer_groups],
                sections=[x.name for x in self.sections],
                src_dir=self.src_dir.location if self.src_dir else None,
            )
        }


def create(term, block):
    return [Layer(name=term.data)]


@reduce(parent_resource=Layer, resource="leap_mn.LayerGroup")
def add_layer_group(layer, layer_group):
    if layer.is_root:
        layer.layer_groups.append(layer_group)


@reduce(parent_resource=Layer, resource="leap_mn.SrcDir")
def add_layer(layer, src_dir):
    if layer.is_root:
        layer.src_dir = src_dir


tags = ["layer"]
