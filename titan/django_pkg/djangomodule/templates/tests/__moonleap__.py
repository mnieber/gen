from moonleap import u0
from titan.api_pkg.apiregistry import get_api_reg

field_name_block_list = ["sortPos", "id"]


def _get_faker_value(field_spec):
    if field_spec.field_type == "boolean":
        return f"f.boolean()"

    if field_spec.field_type == "int":
        return f"f.random_int()"

    if field_spec.field_type == "float":
        return f"f.random_number(digits=2)"

    if field_spec.field_type in ("string", "text", "slug"):
        return f"f.word()"

    if field_spec.field_type in ("string[]", "tags"):
        return f"[f.word(), f.word()]"

    if field_spec.field_type == "int[]":
        return f"[f.random_int(), f.random_int()]"

    if field_spec.field_type == "uuid":
        return f"f.uuid4()"

    if field_spec.field_type == "uuid[]":
        return f"[f.uuid4(), f.uuid4()]"

    if field_spec.field_type == "date":
        return f"f.date()"

    if field_spec.field_type == "json":
        return "{}"

    if field_spec.field_type == "image":
        return '"image.jpg"'

    if field_spec.field_type == "markdown":
        return '"# " + f.word()'

    if field_spec.field_type == "url":
        return "'www.example.com'"

    raise Exception(f"Cannot deduce faker function for {field_spec.field_type}")


def get_helpers(_):
    class Helpers:
        def has_form(self, django_model):
            for api_spec in get_api_reg().api_specs():
                for item_name_saved, is_list in api_spec.saves:
                    if django_model.type_spec.type_name == u0(item_name_saved):
                        return True
            return False

        def get_field_specs(self, type_spec):
            return [
                x
                for x in type_spec.get_field_specs()
                if "server" in x.has_model
                # and "server" not in x.optional
                and x.name not in field_name_block_list and x.field_type != "relatedSet"
            ]

        def get_faker_value(self, field_spec):
            return _get_faker_value(field_spec)

    return Helpers()
