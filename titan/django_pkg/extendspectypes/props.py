from moonleap import upper0
from moonleap.resources.type_spec_store import FieldSpec, TypeSpec, type_spec_store


def fk_type_spec(self: FieldSpec):
    target = self.field_type_attrs.get("target")
    if not target:
        return None

    return type_spec_store.get(target)


def tn_graphene(self: TypeSpec):
    return f"{upper0(self.type_name)}Type"


def tn_django_model(self: TypeSpec):
    return f"{upper0(self.type_name)}"
