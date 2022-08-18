from moonleap import u0
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec
from titan.api_pkg.typeregistry import get_type_reg


def tn_graphene(self: TypeSpec):
    return f"{u0(self.type_name)}T"


def graphene_type(self: FieldSpec, args):
    infix = ", " if args else ""
    if self.field_type == "relatedSet":
        return f"graphene.List({self.target_type_spec.tn_graphene}{infix}{args})"

    if self.field_type == "fk":
        return f"graphene.Field({self.target_type_spec.tn_graphene}{infix}{args})"

    if self.field_type in ("form"):
        return f"{self.target_type_spec.tn_graphene}({args})"

    if self.field_type == "boolean":
        return f"graphene.Boolean({args})"

    if self.field_type == "int":
        return f"graphene.Int({args})"

    if self.field_type == "float":
        return f"graphene.Float({args})"

    if self.field_type in ("string", "text", "slug"):
        return f"graphene.String({args})"

    if self.field_type == "string[]":
        return f"graphene.List(graphene.String{infix}{args})"

    if self.field_type == "uuid":
        return f"graphene.ID({args})"

    if self.field_type == "idList":
        return f"graphene.List(graphene.String)"

    if self.field_type in ("any", "json"):
        return f"GenericScalar({args})"

    raise Exception(f"Cannot deduce arg type for {self.field_type}")


def target_item(self):
    if self.target is None:
        return None

    for item in get_type_reg().items:
        if item.type_name == self.target:
            return item

    raise Exception(f"Cannot find target item for {self.target}")
