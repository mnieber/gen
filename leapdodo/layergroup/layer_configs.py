from leapdodo.layer import LayerConfig


def get(layer_group):
    def inner():
        return dict(
            LAYER_GROUPS={
                layer_group.name: [{layer.name: dict()} for layer in layer_group.layers]
            }
        )

    return LayerConfig(body=lambda x: inner())
