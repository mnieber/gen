import os

import ramda as R
from moonleap import u0
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def _on_delete(field):
    return (
        "models.CASCADE"
        if field.field_type_attrs.get("on_delete", "") == "cascade"
        else "models.SET_NULL"
    )


def _model(field):
    t = field.field_type

    null_blank = [] if field.required else ["null=True", "blank=True"]
    unique = ["unique=True"] if field.unique else []
    help_text = [f"help_text='{field.description}'"] if field.description else []

    if t == "fk":
        on_delete = _on_delete(field)
        related_name = (
            ['related_name="+"']
            if not field.field_type_attrs.get("has_related_set", True)
            else []
        )
        args = [
            u0(field.field_type_attrs["target"]),
            f"on_delete={on_delete}",
            *null_blank,
            *related_name,
            *unique,
            *help_text,
        ]
        return f"models.ForeignKey({', '.join(args)})"

    if t == "string":
        max_length = field.field_type_attrs.get("max_length")
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        if max_length is not None:
            args = [
                f"max_length={max_length}",
                *default_arg,
                *null_blank,
                *unique,
                *help_text,
            ]
            return f"models.CharField({', '.join(args)})"
        else:
            args = [*default_arg, *null_blank, *unique, *help_text]
            return f"models.TextField({', '.join(args)})"

    if t == "json":
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        args = [*default_arg, *null_blank, *unique, *help_text]
        return f"models.JSONField({', '.join(args)})"

    if t in ("slug", "url"):
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        max_length = field.field_type_attrs.get("max_length")
        max_length_arg = [f"max_length={max_length}"] if max_length else []

        args = [*default_arg, *max_length_arg, *null_blank, *unique, *help_text]
        model = "SlugField" if t == "slug" else "URLField"
        return f"models.{model}({', '.join(args)})"

    if t == "boolean":
        default_arg = (
            [f'default={"True" if field.default_value else "False"}']
            if field.default_value in (True, False)
            else []
        )
        args = [*default_arg, *null_blank, *help_text]
        return f"models.BooleanField({', '.join(args)})"

    if t == "uuid":
        args = [*null_blank, *help_text]
        return f"models.UUIDField({', '.join(args)})"

    if t == "email":
        default_arg = (
            [f'default="{field.default_value}"'] if field.default_value else []
        )
        args = [*default_arg, *null_blank, *unique, *help_text]
        return f"models.EmailField({', '.join(args)})"

    if t == "date":
        args = [*unique, *help_text]
        return f"models.DateField({', '.join(args)})"

    raise Exception(f"Unknown model field type: {t}")


def _field_specs(type_spec):
    return sorted(
        [x for x in type_spec.field_specs if x.name_snake != "id"],
        key=lambda x: x.name_snake,
    )


class Sections:
    def __init__(self, res):
        self.res = res

    def model_imports(self, item_name):
        result = []
        type_spec = ml_type_spec_from_item_name(item_name)
        for field_spec in _field_specs(type_spec):
            if field_spec.field_type == "fk":
                fk_item_name = field_spec.field_type_attrs["target"]
                fk_item_type = u0(fk_item_name)
                for module in self.res.django_app.modules:
                    if fk_item_name in [x.name for x in module.item_types]:
                        result.append(
                            f"from {module.name_snake}.models import {fk_item_type}"
                        )

        return "\n".join(result)

    def model_fields(self, item_name):
        result = []
        indent = "    "
        type_spec = ml_type_spec_from_item_name(item_name)
        for field_spec in _field_specs(type_spec):
            if field_spec.field_type == "related_set":
                continue
            model = _model(field_spec)
            result.append(indent + f"{field_spec.name_snake} = {model}")

        return "\n".join(result or [indent + "pass"])

    def str_repr(self, item_name):
        indent = " " * 6
        type_spec = ml_type_spec_from_item_name(item_name)
        for field_spec in _field_specs(type_spec):
            if field_spec.field_type == "string":
                return (
                    f"{indent}return '{u0(item_name)}: ' + self.{field_spec.name_snake}"
                )

        return ""

    def import_item_types(self):
        result = []

        for item_type in self.res.item_types:
            module = R.head(item_type.django_modules)
            if module:
                result.append(
                    f"from {module.name_snake}.models import {item_type.name}"
                )

        return os.linesep.join(result)


def get_context(self):
    return dict(sections=Sections(self))
