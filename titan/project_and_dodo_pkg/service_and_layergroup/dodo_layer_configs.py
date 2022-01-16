from titan.dodo_pkg.layer import LayerConfig


def get(layer_group):
    def inner():
        result = dict(
            DIAL={
                "default": {
                    str(i + 1): f"dodo {layer.name}."
                    for i, layer in enumerate(layer_group.layers)
                },
                "shift": {
                    str(i + 1): r"${/ROOT/src_dir}/" + ("" if i == 0 else layer.name)
                    for i, layer in enumerate(layer_group.layers)
                },
                "ctrl": {
                    "1": r"${/ROOT/project_dir}/",
                    "2": r"${/ROOT/config_dir}/",
                    "3": r"~/",
                },
            }
        )
        if len(layer_group.layers) < 12:
            pos = min(max(6, len(layer_group.layers)), 12)
            result["DIAL"]["default"][str(pos)] = "dodo stack.browse --url "
        return result

    return LayerConfig(body=lambda x: inner())
