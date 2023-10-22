def get_meta_data_by_fn(_, __):
    return {
        "auth.py": {
            "include": bool(_.django_app.user_accounts_module),
        },
    }
