def get_meta_data_by_fn(_, __):
    return {
        "case.py": {
            "include": bool(_.django_app.use_translation),
        },
    }
