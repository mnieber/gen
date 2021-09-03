from moonleap.resources.data_type_spec_store import FK, RelatedSet, data_type_spec_store
from moonleap.utils.case import camel_to_snake, lower0


def _on_delete(field):
    return (
        "models.CASCADE"
        if field.spec.get("onDelete", "") == "cascade"
        else "models.SET_NULL"
    )


def _model(field):
    t = field.field_type

    null_blank = [] if field.required else [f"null=True", f"blank=True"]
    unique = ["unique=True"] if field.unique else []

    if isinstance(t, FK):
        on_delete = _on_delete(field)
        args = [t.target, f"on_delete={on_delete}", *null_blank, *unique]
        return f"models.ForeignKey({', '.join(args)})"

    if t == "string":
        max_length = field.spec.get("maxLength", None)
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        if max_length is not None:
            args = [f"max_length={max_length}", *default_arg, *null_blank, *unique]
            return f"models.CharField({', '.join(args)})"
        else:
            args = [*default_arg, *null_blank, *unique]
            return f"models.TextField({', '.join(args)})"

    if t == "json":
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        args = [*default_arg, *null_blank, *unique]
        return f"models.JSONField({', '.join(args)})"

    if t in ("slug", "url"):
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        max_length = field.spec.get("maxLength", None)
        max_length_arg = [f"max_length={max_length}"] if max_length else []

        args = [*default_arg, *max_length_arg, *null_blank, *unique]
        model = "SlugField" if t == "slug" else "URLField"
        return f"models.{model}({', '.join(args)})"

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
        args = [*default_arg, *null_blank, *unique]
        return f"models.EmailField({', '.join(args)})"

    if t == "date":
        args = [*unique]
        return f"models.DateField({', '.join(args)})"

    raise Exception(f"Unknown model field type: {t}")


def _fields(spec):
    return sorted(
        [x for x in spec.fields if x.name_snake != "id"], key=lambda x: x.name_snake
    )


class Sections:
    def __init__(self, res):
        self.res = res

    def model_imports(self, item_name):
        result = []
        spec = data_type_spec_store.get_spec(item_name)
        for field in _fields(spec):
            if isinstance(field.field_type, FK):
                fk_item_type = field.field_type.target
                fk_item_name = lower0(fk_item_type)
                for module in self.res.django_app.modules:
                    if fk_item_name in [
                        x.item_name for x in module.item_lists_provided
                    ]:
                        result.append(
                            f"from {module.name_snake}.models import {fk_item_type}"
                        )

        return "\n".join(result)

    def model_fields(self, item_name):
        result = []
        indent = "    "
        spec = data_type_spec_store.get_spec(item_name)
        for field in _fields(spec):
            if isinstance(field.field_type, RelatedSet):
                continue
            model = _model(field)
            result.append(indent + f"{field.name_snake} = {model}")

        return "\n".join(result or [indent + "pass"])
