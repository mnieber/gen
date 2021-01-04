from moonleap import Resource, tags


class LayerGroup(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.layer_by_name = {}


@tags(["layer-group"])
def create(term, block):
    return [LayerGroup(name=term.data)]


is_ittable = True
