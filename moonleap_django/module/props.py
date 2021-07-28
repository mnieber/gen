from moonleap.resources.data_type_spec_store import data_type_spec_store


def _model(field):
    t = field.spec["type"]
    if t == "string":
        max_length = field.spec.get("maxLength", None)
        if max_length is not None:
            return f"models.CharField(max_length={max_length})"
        else:
            return f"models.TextField()"
    raise Exception(f"Unknown field type: {t}")


def _fields(spec):
    return [x for x in spec.fields if x.name_snake != "id"]


def p_section_fields(self, item_type):
    result = []
    indent = "    "
    spec = data_type_spec_store.get_spec(item_type.name)
    for field in _fields(spec):
        model = _model(field)
        result.append(indent + f"{field.name_snake} = {model}")

    return "\n".join(result)
