import os

import ramda as R
from moonleap import u0
from moonleap.utils.case import sn
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name
from titan.django_pkg.graphene_django.utils import find_module_that_provides_item_list


def _on_delete(field):
    return (
        "models.CASCADE"
        if field.field_type_attrs.get("onDelete", "") == "cascade"
        else "models.SET_NULL"
    )


def _model(field, item_name):
    t = field.field_type

    null_blank = [] if field.required else ["null=True", "blank=True"]
    unique = ["unique=True"] if field.unique else []
    help_text = [f"help_text='{field.description}'"] if field.description else []

    if t == "fk":
        through = field.through
        on_delete = _on_delete(field)

        related_name = (
            ['related_name="+"']
            if not field.field_type_attrs.get("hasRelatedSet", True)
            else [f'related_name="{sn(item_name)}_set"']
        )
        through = (
            [f'through="{through}"']
            if field.field_type_attrs.get("through", "")
            else []
        )
        args = [
            u0(field.target),
            *([] if through else [f"on_delete={on_delete}"]),
            *through,
            *([] if through else null_blank),
            *related_name,
            *unique,
            *help_text,
        ]
        return f"models.{'ManyToManyField' if through else 'ForeignKey'}({', '.join(args)})"

    if t == "string":
        max_length = field.field_type_attrs.get("maxLength")
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
        max_length = field.field_type_attrs.get("maxLength")
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
        [x for x in type_spec.field_specs if x.name != "id"],
        key=lambda x: x.name,
    )


def get_context(module):
    _ = lambda: None
    _.django_app = module.django_app

    class Sections:
        def model_imports(self, item_name):
            result = []
            type_spec = ml_type_spec_from_item_name(item_name)
            for field_spec in type_spec.get_field_specs(["fk"]):
                provider_module = find_module_that_provides_item_list(
                    _.django_app, field_spec.target
                )
                if provider_module:
                    result.append(
                        f"from {sn(provider_module.name)}.models "
                        + f"import {u0(field_spec.target)}"
                    )

            return "\n".join(result)

        def model_fields(self, item_name):
            result = []
            indent = "    "
            type_spec = ml_type_spec_from_item_name(item_name)
            for field_spec in _field_specs(type_spec):
                if field_spec.field_type == "relatedSet":
                    continue
                model = _model(field_spec, item_name)
                result.append(indent + f"{sn(field_spec.name)} = {model}")

            return "\n".join(result or [indent + "pass"])

        def repr_function(self, item_name):
            indent = " " * 4
            type_spec = ml_type_spec_from_item_name(item_name)
            for field_spec in _field_specs(type_spec):
                if field_spec.field_type == "string":
                    return (
                        f"{indent}def __str__(self):\n"
                        + f"{indent}  return '{u0(item_name)}: ' + self."
                        + f"{sn(field_spec.name)}"
                    )

            return ""

        def import_item_types(self):
            result = []

            for item_list in module.item_lists_provided:
                result.append(
                    f"from {sn(module.name)}.models import {item_list.item_name}"
                )

            return os.linesep.join(result)

    return dict(sections=Sections())
