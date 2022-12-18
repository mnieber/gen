from titan.widgets_pkg.pkg.load_widget_specs.create_widget_spec import (
    create_widget_spec,
)


def get_place_dict(src_dict, place):
    for k, v in src_dict.items():
        ws, _ = create_widget_spec(k, v, None)
        if ws.place == place:
            return {k: v}
    return None
