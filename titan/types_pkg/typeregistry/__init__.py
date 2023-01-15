from moonleap.session import get_session
from titan.typespec.load_type_specs import load_type_specs

from .resources import TypeRegistry

_type_registry = None


def get_type_reg():
    global _type_registry
    if not _type_registry:
        _type_registry = TypeRegistry()
        load_type_specs(_type_registry, get_session().spec_dir)

    return _type_registry
