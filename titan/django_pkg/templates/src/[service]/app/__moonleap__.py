def get_meta_data_by_fn(_, __):
    return {
        "templatetags": {
            "include": bool(_.django_app.use_translation),
        },
        "tr.py.j2": {
            "include": bool(_.django_app.use_translation),
        },
    }
