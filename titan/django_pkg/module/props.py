from moonleap.resources.data_type_spec_store import FK, data_type_spec_store


def _on_delete(field):
    return (
        "models.CASCADE"
        if field.spec.get("onDelete", "") == "cascade"
        else "models.SET_NULL"
    )


def _model(field):
    t = field.field_type

    if isinstance(t, FK):
        flag = "False" if field.required else "True"
        on_delete = _on_delete(field)
        return (
            f"models.ForeignKey({t.target}, on_delete={on_delete}, "
            + f"null={flag}, blank={flag})"
        )

    if t == "string":
        max_length = field.spec.get("maxLength", None)
        if max_length is not None:
            return f"models.CharField(max_length={max_length})"
        else:
            return r"models.TextField()"

    if t == "bool":
        return r"models.BooleanField()"

    if t == "email":
        return r"models.EmailField()"

    if t == "date":
        return r"models.DateField()"

    raise Exception(f"Unknown model field type: {t}")


def _fields(spec):
    return [x for x in spec.fields if x.name_snake != "id"]


def p_section_model_fields(self, item_name):
    result = []
    indent = "    "
    spec = data_type_spec_store.get_spec(item_name)
    for field in _fields(spec):
        model = _model(field)
        result.append(indent + f"{field.name_snake} = {model}")

    return "\n".join(result or [indent + "pass"])
