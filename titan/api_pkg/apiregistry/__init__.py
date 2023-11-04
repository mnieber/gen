from moonleap.session import get_session
from titan.api_pkg.pkg.load_api_specs import load_api_specs

from .resources import ApiRegistry

_api_registry = None


def get_api_reg():
    global _api_registry
    if not _api_registry:
        _api_registry = ApiRegistry()
        load_api_specs(_api_registry, get_session().ws.spec_dir)

    return _api_registry
