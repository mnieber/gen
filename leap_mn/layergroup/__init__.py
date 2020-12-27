from leap_mn.resource import Resource


class LayerGroup(Resource):
    def __init__(self, name):
        self.name = name
        self.layer_by_name = {}

    def describe(self, indent):
        return (
            " " * indent
            + f"LayerGroup: name={self.name}"
            + "\n"
            + "\n".join([x.describe(indent + 4) for x in self.layer_by_name.values()])
        )


def create(term, line, block):
    return LayerGroup(name=term.data)


def add_layers(resource, term, block):
    for line in block.find_lines_with_term(term):
        for a_term in line.find_terms_with_tag("layer"):
            layer = block.get_resource(a_term)
            resource.layer_by_name[layer.name] = layer
