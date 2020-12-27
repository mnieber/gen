from leap_mn.resource import Resource


class Layer(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self, indent):
        return " " * indent + f"Layer: name={self.name}"


def create(term, line, block):
    return Layer(name=term.data)


# def add_layer():
#     def action(term, line, block):
#         layer = Layer(term.data)

#         layer_group_terms = line.find_terms_with_tag(left_of=term, tag="layer-group")
#         if layer_group_terms:
#             layer_group_term = layer_group_terms[-1]
#             layer_group = LayerGroups.global_group(config).group_by_name[layer_group_term.data]
#         else:
#             layer_group = LayerGroup.global_group(config)

#         layer_group.layer_by_name.setdefault(layer.name, layer)

#     return action
