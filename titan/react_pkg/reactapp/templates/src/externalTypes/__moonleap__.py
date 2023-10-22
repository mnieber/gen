def get_meta_data_by_fn(_, __):
    return {
        "react-keyboard-event-handler.d.ts": {
            "include": bool(_.react_app.has_flag("app/keyboardHandler")),
        },
    }
