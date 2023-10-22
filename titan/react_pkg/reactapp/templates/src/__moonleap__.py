def get_meta_data_by_fn(_, __):
    return {
        "reportWebVitals.ts": {
            "include": bool(_.react_app.has_flag("app/reportWebVitals")),
        },
    }
