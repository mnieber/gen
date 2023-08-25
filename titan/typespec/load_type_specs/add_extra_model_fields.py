from moonleap.utils.fp import append_uniq


def add_extra_model_fields(type_spec, value):
    new_value = dict()
    if (
        type_spec.is_entity
        and not type_spec.get_field_spec_by_key("id")
        and not value.get("id")
    ):
        new_value["id"] = "Id,primary_key"

    if (
        type_spec.is_sorted
        and not type_spec.get_field_spec_by_key("sortPos")
        and not value.get("sortPos")
    ):
        new_value["sortPos"] = "Int = 0"

    if not new_value:
        return

    new_value.update(value)
    if new_value.get("sortPos"):
        api_spec = new_value.setdefault("__api__", {})
        deleted_fields = api_spec.setdefault("__delete__", [])
        append_uniq(deleted_fields, "sortPos")

    for key in list(value.keys()):
        del value[key]

    value.update(new_value)
