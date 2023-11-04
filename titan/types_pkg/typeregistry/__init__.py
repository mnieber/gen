from moonleap.session import get_session

from .resources import TypeRegistry

_type_registry = None


def get_type_reg():
    global _type_registry
    if not _type_registry:
        from titan.typespec.load_type_specs import load_type_specs

        _type_registry = TypeRegistry()
        load_type_specs(_type_registry, get_session().ws.spec_dir)

    return _type_registry
