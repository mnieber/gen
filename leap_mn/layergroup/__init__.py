import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from moonleap import Resource, tags


class LayerGroup(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


def get_layer_config(layer_group):
    result = {layer_group.name: [{layer.name: dict()} for layer in layer_group.layers]}
    return result


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=term.data)
    layer_group.add_child(
        LayerConfig(lambda x: dict(LAYER_GROUPS=get_layer_config(layer_group)))
    )
    return layer_group


def meta():
    from leap_mn.layer import Layer
    from leap_mn.project import Project

    return {
        LayerGroup: dict(props={"layers": props.children_of_type(Layer)}),
    }


def add_layer_group_to_project(project, layer_group):
    if project.config_layer:
        project.config_layer.add_child(layer_group)


rules = {
    "project": {("has", "layer-group"): add_layer_group_to_project},
}
