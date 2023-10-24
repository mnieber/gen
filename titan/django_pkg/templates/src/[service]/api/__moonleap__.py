from titan.api_pkg.apiregistry import get_api_reg


def get_contexts(_):
    if not _.django_app.api_module:
        return []
    return [dict(api_reg=get_api_reg())]
