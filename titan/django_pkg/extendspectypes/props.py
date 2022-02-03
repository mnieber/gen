from moonleap import u0
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec
from titan.django_pkg.graphene_django.utils import find_module_that_provides_item_list


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
    if self.field_type == "relatedSet":
        return f"graphene.List({self.target_type_spec.tn_graphene}{args})"

    if self.field_type == "fk":
        return f"graphene.Field({self.target_type_spec.tn_graphene}{args})"

    if self.field_type in ("form"):
        return f"{self.target_type_spec.tn_graphene}({args})"

    return self.graphene_input_type


def target_django_module(self, django_app):
    item_name = self.target
    return (
        find_module_that_provides_item_list(django_app, item_name)
        if item_name
        else None
    )
