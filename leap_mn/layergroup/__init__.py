import moonleap.props as props
from moonleap import Resource, tags


class LayerGroup(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["layer-group"], is_ittable=True)
def create_layer_group(term, block):
    return [LayerGroup(name=term.data)]


def meta():
    from leap_mn.layer import Layer

    return {LayerGroup: dict(props={"layers": props.children_of_type(Layer)})}
