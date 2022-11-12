from titan.api_pkg.apiregistry import get_api_reg


def api_spec(self):
    return get_api_reg().get(self.name)
