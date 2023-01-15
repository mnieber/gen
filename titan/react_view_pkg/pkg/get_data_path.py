def get_data_path(widget_spec, obj):
    ws = widget_spec
    while ws:
        if data_path := ws.get_data_path(obj=obj):
            return data_path
        ws = ws.parent
    return None
