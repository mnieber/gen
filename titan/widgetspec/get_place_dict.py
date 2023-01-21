from moonleap import is_private_key


def get_place_dict(src_dict, place):
    from titan.widgetspec.load_widget_specs.create_widget_spec import create_widget_spec

    for k, v in src_dict.items():
        if is_private_key(k):
            continue
        ws, _ = create_widget_spec(k, v, None)
        if ws.place == place:
            return {k: v}
    return None
