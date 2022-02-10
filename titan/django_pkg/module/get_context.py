import os

from moonleap import u0
from moonleap.utils.case import sn
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
        if field.through:
            raise Exception(
                f"Fk fields cannot use 'through'. Use a relatedSet field instead. "
                + f"For field: {field.name} in type: {item_name}"
            )

        on_delete = _on_delete(field)

        related_name = (
            ['related_name="+"']
            if not field.field_type_attrs.get("hasRelatedSet", True)
            else [f'related_name="{sn(item_name)}_set"']
        )

        args = [
            field.target,
            f"on_delete={on_delete}",
            *null_blank,
            *related_name,
            *unique,
            *help_text,
        ]
        return f"models.ForeignKey({', '.join(args)})"

    if t == "relatedSet":
        if not field.through:
            return None

        related_name = (
            ['related_name="+"']
            if not field.field_type_attrs.get("hasRelatedSet", True)
            else [f'related_name="{sn(item_name)}_set"']
        )

        args = [
            field.target,
            f'through="{field.through}"',
            *related_name,
            *unique,
            *help_text,
        ]
        return f"models.ManyToManyField({', '.join(args)})"

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

    if t == "int":
        default_arg = (
            [f"default={field.default_value}"]
            if field.default_value is not None
            else []
        )
        args = [*default_arg, *null_blank, *help_text]
        return f"models.IntegerField({', '.join(args)})"

    if t == "float":
        default_arg = (
            [f"default={field.default_value}"]
            if field.default_value is not None
            else []
        )
        args = [*default_arg, *null_blank, *help_text]
        return f"models.FloatField({', '.join(args)})"

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
        def model_imports(self, item_list):
            result = []
            targets = []
            for field_spec in item_list.type_spec.get_field_specs(["fk"]):
                targets.append(field_spec.target)

            for inline_model in self.get_inline_models(item_list):
                targets.append(inline_model)

            for target in targets:
                provider_module = find_module_that_provides_item_list(
                    _.django_app, target
                )
                if provider_module:
                    result.append(
                        f"from {sn(provider_module.name)}.models import {target}"
                    )
            return "\n".join(result)

        def model_fields(self, item_list):
            result = []
            indent = "    "
            for field_spec in _field_specs(item_list.type_spec):
                model = _model(field_spec, item_list.item_name)
                if model:
                    result.append(indent + f"{sn(field_spec.name)} = {model}")

            return "\n".join(result or [indent + "pass"])

        def repr_function(self, item_list):
            indent = " " * 4
            for field_spec in _field_specs(item_list.type_spec):
                if field_spec.field_type == "string":
                    return (
                        f"{indent}def __str__(self):\n"
                        + f"{indent}  return '{u0(item_list.item_name)}: ' + self."
                        + f"{sn(field_spec.name)}"
                    )

            return ""

        def get_inline_models(self, item_list):
            return [
                x.target
                for x in item_list.type_spec.get_field_specs(["relatedSet"])
                if x.through
            ]

        def import_item_types(self):
            result = []

            for item_list in module.item_lists_provided:
                result.append(
                    f"from {sn(module.name)}.models import {item_list.item_name}"
                )

            return os.linesep.join(result)

    return dict(sections=Sections())
