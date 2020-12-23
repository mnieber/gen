from resources.resource import Resource


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


class Builder:
    @staticmethod
    def create(term, line, block):
        return LayerGroup(name=term.data)

    @staticmethod
    def build(resource, term, line, block):
        __import__("pudb").set_trace()
        for a_term in line.terms:
            if a_term.tag == "layer":
                layer = block.get_resource(a_term)
                resource.layer_by_name[layer.name] = layer
