def get_meta_data_by_fn(_, __):
    return {
        "routeTable.ts.j2": {
            "include": bool(_.module.routes),
        },
        "navEvents.ts": {
            "include": bool(_.module.routes),
        },
    }
