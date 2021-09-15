from moonleap.resources.type_spec_store import type_spec_store
from moonleap.utils.case import upper0
from moonleap.utils.inflect import plural


def _field_specs(type_spec):
    return [x for x in type_spec.field_spec_by_name.values() if x.name_snake != "id"]


def _graphene_field(field, item_name):
    t = field.field_type

    if t == "fk":
        return r"graphene.ID()"

    if t == "string":
        return r"graphene.String()"

    if t == "bool":
        return r"graphene.Boolean()"

    if t in ("email", "slug", "url"):
        return r"graphene.String()"

    if t == "date":
        return r"graphene.types.datetime.Date()"

    raise Exception(f"Unknown graphene field type: {t} in spec for {item_name}")


class TypeSectionsMixin:
    def graphene_fields(self, item_name):
        result = []
        indent = "    "
        type_spec = type_spec_store.get(item_name)
        for field_spec in _field_specs(type_spec):
            graphene_field = _graphene_field(field_spec, item_name)
            result.append(indent + f"{field_spec.name_snake} = {graphene_field}")

        return "\n".join(result or [indent + "pass"])

    def mutation_fields(self, module):
        result = []
        indent = "    "

        for form in module.forms:
            result.append(
                indent + f"{form.item_name_snake} = {upper0(form.item_name)}.Field()"
            )

        for item in module.items_received:
            result.append(
                indent
                + f"post_{item.item_name_snake} = Post{upper0(item.item_name)}.Field()"
            )

        return "\n".join(result or [indent + "pass"])

    def query_base_types(self, module):
        result = []

        for item_list in module.item_lists_provided:
            result.append(f"{upper0(plural(item_list.item_name))}Query, ")

        return "".join(result + (["graphene.ObjectType"] if result else []))
