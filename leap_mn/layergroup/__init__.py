from leap_mn.resource import Resource


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
    return LayerGroup(name=term.data)


create_rule_by_tag = {
    "layer-group": create,
}


is_ittable_by_tag = {
    "layer-group": True,
}
