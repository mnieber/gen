def get_group_layer_config(layer_group):
    result = {layer_group.name: [{layer.name: dict()} for layer in layer_group.layers]}
    return dict(LAYER_GROUPS=result)
