from leap_mn.layergroup import LayerGroup
from leap_mn.resource import Resource


class LayerGroups(Resource):
    def __init__(self):
        self.group_by_name = {"global": LayerGroup("global")}

    def describe(self, indent=0):
        return (
            " " * indent
            + "LayerGroups:\n"
            + "\n".join([x.describe(indent + 4) for x in self.group_by_name.values()])
        )


# def add_layer_group(term, line, block):
#     layer_group = LayerGroup()
#     LayerGroups.global_group(config).group_by_name.setdefault(
#         layer_group.name, layer_group
#     )


create_rule_by_tag = {}
