def get_named_item_list_pipeline(widget_spec):
    ws = widget_spec
    while ws:
        if pipeline := ws.get_pipeline_by_name("items"):
            return pipeline
        ws = ws.parent
    return None


def get_named_item_pipeline(widget_spec):
    ws = widget_spec
    while ws:
        if pipeline := ws.get_pipeline_by_name("item"):
            return pipeline
        ws = ws.parent
    return None
