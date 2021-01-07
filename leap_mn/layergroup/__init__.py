from moonleap import Resource, tags


class LayerGroup(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["layer-group"], is_ittable=True)
def create_layer_group(term, block):
    return [LayerGroup(name=term.data)]


meta = {}
