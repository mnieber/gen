def get_meta_data_by_fn(_, __):
    return {
        ".": {"name": f"../{_.module.name}"},
        "routeTable.ts.j2": {
            "include": bool(_.module.routes),
        },
        "navFunctions.ts": {
            "include": bool(_.module.routes),
        },
    }


def get_contexts(_):
    return [dict(module=module) for module in _.react_app.modules]
