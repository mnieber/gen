def get_meta_data_by_fn(_, __):
    return {
        "ValuePicker.tsx": {
            "include": bool(_.react_app.has_flag("utils/ValuePicker")),
        },
        "ValuePicker.index.tsx": {
            "include": bool(_.react_app.has_flag("utils/ValuePicker")),
            "name": "index.tsx",
        },
    }
