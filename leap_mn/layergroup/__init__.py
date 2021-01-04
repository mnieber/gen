from moonleap import Resource


class LayerGroup(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.layer_by_name = {}

    def describe(self):
        return dict(
            name=self.name,
            layers=[x.name for x in self.layer_by_name.values()],
        )


def create(term, block):
    return [LayerGroup(name=term.data)]


is_ittable = True


tags = ["layer-group"]
