from moonleap import u0
from moonleap.resources.type_spec_store import TypeSpec


def tn_graphene(self: TypeSpec):
    return f"{u0(self.type_name)}Type"
