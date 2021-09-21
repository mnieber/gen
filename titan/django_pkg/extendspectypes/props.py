from moonleap import upper0
from moonleap.resources.type_spec_store import TypeSpec


def tn_graphene(self: TypeSpec):
    return f"{upper0(self.type_name)}Type"


def tn_django_model(self: TypeSpec):
    return f"{upper0(self.type_name)}"
