from leap_mn.resource import Resource


class Layer(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self):
        return {str(self): dict(name=self.name)}


def create(term, line, block):
    return Layer(name=term.data)


create_rule_by_tag = {
    "layer": create,
}

update_rules = [
    ("leap_mn.layergroup", "layergroup"),
]
