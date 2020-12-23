from config import config

from resources.resource import Resource


class LayerGroups(Resource):
    def __init__(self):
        self.group_by_name = {"global": LayerGroup()}

    @staticmethod
    def global_group(config):
        return config.global_block.resource_by_name.setdefault(
            "layer-groups", LayerGroups()
        )

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
