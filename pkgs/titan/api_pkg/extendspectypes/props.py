from typespec.field_spec import FieldSpec
from typespec.type_spec import TypeSpec

from moonleap import u0


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

    if self.field_type == "int[]":
        return f"graphene.List(graphene.Int{infix}{args})"

    if self.field_type == "float":
        return f"graphene.Float({args})"

    if self.field_type in ("string", "text", "slug", "markdown"):
        return f"graphene.String({args})"

    if self.field_type == "string[]":
        return f"graphene.List(graphene.String{infix}{args})"

    if self.field_type == "uuid":
        return f"graphene.ID({args})"

    if self.field_type == "uuid[]":
        return f"graphene.List(graphene.String{infix}{args})"

    if self.field_type in ("any", "json"):
        return f"GenericScalar({args})"

    raise Exception(f"Cannot deduce arg type for {self.field_type}")


def field_spec_graphql_type(self: FieldSpec, host):
    postfix = "" if self.is_optional(host) else "!"

    if self.field_type in (
        "string",
        "text",
        "json",
        "url",
        "slug",
        "image",
        "markdown",
    ):
        return "String" + postfix

    if self.field_type in ("boolean",):
        return "Boolean" + postfix

    if self.field_type in ("int",):
        return "Int" + postfix

    if self.field_type in ("string[]",):
        return "[String]" + postfix

    if self.field_type in ("int[]",):
        return "[Int]" + postfix

    if self.field_type in ("float",):
        return "Float" + postfix

    if self.field_type in ("uuid",):
        return "ID" + postfix

    if self.field_type in ("uuid[]",):
        return "[String]" + postfix

    if self.field_type in ("form",):
        return f"{self.target_type_spec.type_name}T" + postfix

    raise Exception(f"Cannot deduce graphql type for {self.field_type}")