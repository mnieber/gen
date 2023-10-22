def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "include": bool(_.django_app.add_tests),
        }
    }
