def get_meta_data_by_fn(_, __):
    return {
        "useScheduledCall.ts": {
            "include": bool(_.react_app.has_flag("utils/useScheduledCall")),
        },
        "useScheduledCall.index.ts": {
            "include": bool(_.react_app.has_flag("utils/useScheduledCall")),
            "name": "index.ts",
        },
        "useValuePickerState.ts": {
            "include": bool(_.react_app.has_flag("utils/ValuePicker")),
        },
        "useValuePickerState.index.ts": {
            "include": bool(_.react_app.has_flag("utils/ValuePicker")),
            "name": "index.ts",
        },
    }
