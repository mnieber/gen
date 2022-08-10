from moonleap import u0
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec
from titan.api_pkg.typeregistry import get_type_reg


def tn_graphene(self: TypeSpec):
    return f"{u0(self.type_name)}Type"


def graphene_input_type(self: FieldSpec):
    if self.field_type == "boolean":
        return f"graphene.Boolean()"

    if self.field_type == "int":
        return f"graphene.Int()"

    if self.field_type == "float":
        return f"graphene.Float()"

    if self.field_type in ("string", "slug", "json"):
        return f"graphene.String()"

    if self.field_type == "uuid":
        return f"graphene.ID()"

    if self.field_type == "idList":
        return f"graphene.List(graphene.String)"

    if self.field_type == "any":
        return f"GenericScalar()"

    raise Exception(f"Cannot deduce arg type for {self.field_type}")


def graphene_output_type(self: FieldSpec, args):
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

    if self.field_type in ("string", "slug"):
        return f"graphene.String({args})"

    if self.field_type == "uuid":
        return f"graphene.ID({args})"

    if self.field_type == "idList":
        return f"graphene.List(graphene.String)"

    if self.field_type in ("any", "json"):
        return f"GenericScalar({args})"

    raise Exception(f"Cannot deduce arg type for {self.field_type}")


def target_item_type(self):
    return get_type_reg().get_item_type_by_name(self.target) if self.target else None
