def get_meta_data_by_fn(_, __):
    return {
        "cookies.ts": {
            "include": bool(_.service.cypress),
        },
        "slugify.ts": {
            "include": bool(_.react_app.has_flag("utils/slugify")),
        },
        "slugify.index.ts": {
            "include": bool(_.react_app.has_flag("utils/slugify")),
            "name": "index.ts",
        },
        "keyEvents.ts": {
            "include": bool(_.react_app.has_flag("app/keyboardHandler")),
        },
        "keyEvents.index.ts": {
            "include": bool(_.react_app.has_flag("app/keyboardHandler")),
            "name": "index.ts",
        },
    }
