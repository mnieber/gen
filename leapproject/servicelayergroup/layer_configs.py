def get_dial_config(layer_group):
    return dict(
        DIAL={
            "default": {
                str(i + 1): f"dodo {layer.name}."
                for i, layer in enumerate(layer_group.layers)
            },
            "shift": {
                str(i + 1): r"${/ROOT/src_dir}/" + ("" if i == 0 else layer.name)
                for i, layer in enumerate(layer_group.layers)
            },
        }
    )
