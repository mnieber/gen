def get_contexts(_):
    if not _.react_app.auth_module:
        return []
    return [dict(module=_.react_app.auth_module)]
