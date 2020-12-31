from moonleap import Resource, reduce


def get_root_config(layer):
    return dict()


class Layer(Resource):
    def __init__(self, name):
        self.name = name
        self.is_root = name == "root"
        self.path = f"config.yaml" if self.is_root else f"{name}.yaml"
        self.layer_groups = []
        self.sections = []
        self.src_dir = None

    def describe(self):
        return dict(
            name=self.name,
            path=self.path,
            layer_groups=[x.name for x in self.layer_groups],
            sections=[x.name for x in self.sections],
            src_dir=self.src_dir.location if self.src_dir else None,
        )


class LayerConfig(Resource):
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def describe(self):
        return dict(name=self.name)


def create(term, block):
    return [Layer(name=term.data)]


@reduce(parent_resource="moonleap.Always", resource=Layer, delay=True)
def add_root_config(always, layer):
    if layer.is_root:
        return [LayerConfig("root", get_root_config(layer))]


@reduce(parent_resource="leap_mn.Layer", resource=LayerConfig)
def add_config(layer, layer_config):
    if layer_config.is_created_in_block_that_mentions(layer):
        layer.sections.append(layer_config)


@reduce(parent_resource=Layer, resource="leap_mn.LayerGroup")
def add_layer_group(layer, layer_group):
    if layer.is_root:
        layer.layer_groups.append(layer_group)


@reduce(parent_resource=Layer, resource="leap_mn.SrcDir")
def add_src_dir(layer, src_dir):
    if layer.is_root:
        layer.src_dir = src_dir


tags = ["layer"]
