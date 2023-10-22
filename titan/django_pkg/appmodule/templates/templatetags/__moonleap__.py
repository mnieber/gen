def get_meta_data_by_fn(_, __):
    return {
        "tr_tags.py": {
            "include": bool(_.django_app.use_translation),
        },
    }
