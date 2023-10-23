from titan.api_pkg.apiregistry import get_api_reg


def get_contexts(_):
    return [dict(api_reg=get_api_reg())]


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "include": bool(_.django_app.api_module),
        }
    }
