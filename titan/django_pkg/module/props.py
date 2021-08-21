from moonleap.resources.data_type_spec_store import FK, data_type_spec_store


def _on_delete(field):
    return (
        "models.CASCADE"
        if field.spec.get("onDelete", "") == "cascade"
        else "models.SET_NULL"
    )


def _model(field):
    t = field.field_type

    null_blank = [] if field.required else [f"null=True", f"blank=True"]

    if isinstance(t, FK):
        on_delete = _on_delete(field)
        args = [t.target, f"on_delete={on_delete}", *null_blank]
        return f"models.ForeignKey({', '.join(args)})"

    if t == "string":
        max_length = field.spec.get("maxLength", None)
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        if max_length is not None:
            args = [f"max_length={max_length}", *default_arg, *null_blank]
            return f"models.CharField({', '.join(args)})"
        else:
            args = [*default_arg, *null_blank]
            return f"models.TextField({', '.join(args)})"

    if t == "bool":
        default_arg = (
            [f'default={"True" if field.default_value else "False"}']
            if field.default_value in (True, False)
            else []
        )
        args = [*default_arg, *null_blank]
        return f"models.BooleanField({', '.join(args)})"

    if t == "email":
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        args = [*default_arg, *null_blank]
        return f"models.EmailField({', '.join(args)})"

    if t == "date":
        return f"models.DateField()"

    raise Exception(f"Unknown model field type: {t}")


def _fields(spec):
    return [x for x in spec.fields if x.name_snake != "id"]


class Sections:
    def __init__(self, res):
        self.res = res

    def model_fields(self, item_name):
        result = []
        indent = "    "
        spec = data_type_spec_store.get_spec(item_name)
        for field in _fields(spec):
            model = _model(field)
            result.append(indent + f"{field.name_snake} = {model}")

        return "\n".join(result or [indent + "pass"])
