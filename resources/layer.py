from config import config

from resources.resource import Resource


class Layer(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self, indent):
        return " " * indent + f"Layer: name={self.name}"


class Builder:
    @staticmethod
    def create(term, line, block):
        return Layer(name=term.data)


def add_layer():
    def action(term, line, block):
        layer = Layer(term.data)

        layer_group_term = line.find_term_left_of(term, tag="layer-group")
        if layer_group_term:
            layer_group = LayerGroups.get(config).group_by_name[layer_group_term.data]
        else:
            layer_group = LayerGroup.get(config)

        layer_group.layer_by_name.setdefault(layer.name, layer)

    return action
