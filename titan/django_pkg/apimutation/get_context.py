import os

from moonleap import u0
from moonleap.utils.case import sn
from moonleap.utils.codeblock import CodeBlock
from titan.django_pkg.graphene_django.utils import (
    get_django_model_imports,
    get_graphene_type_imports,
)


def _mutation_arguments(field_specs):
    result = {}
    for field_spec in field_specs:
        result[sn(field_spec.name)] = field_spec.graphene_output_type(
            f"required={field_spec.required}"
        )
    return result


def get_context(mutation, api_module):
    _ = lambda: None
    _.django_app = api_module.django_app
    _.inputs_type_spec = mutation.inputs_type_spec
    _.outputs_type_spec = mutation.outputs_type_spec
    _.input_field_specs = list(_.inputs_type_spec.field_specs)
    _.output_field_specs = list(_.outputs_type_spec.field_specs)
    _.fk_output_field_specs = _.outputs_type_spec.get_field_specs(["fk"])

    class Sections:
        def mutation_imports(self):
            result = []
            type_specs = [_.inputs_type_spec, _.outputs_type_spec]
            result.extend(get_graphene_type_imports(type_specs))
            result.extend(get_django_model_imports(_.django_app, type_specs))

            return os.linesep.join(result)

        def mutation_outputs(self):
            indent = " " * 4
            result = []

            for field_spec in _.output_field_specs:
                args = ""
                result.append(
                    f"{indent}{sn(field_spec.name)} = {field_spec.graphene_output_type(args)}"
                )

            return os.linesep.join(result)

        def mutation_arguments(self):
            indent = " " * 8
            result = []

            args = _mutation_arguments(_.input_field_specs)
            for field_name, arg in args.items():
                result.append(f"{indent}{field_name} = {arg}")
            if not args:
                result.append(f"{indent}pass")

            return os.linesep.join(result)

        def mutate_function(self):
            root = CodeBlock(style="python", level=1)
            field_names = list([sn(x.name) for x in _.input_field_specs])

            root.IxI("def mutate", ["self", "info"] + field_names, ":")
            body = root.block(1)

            for item_posted in mutation.items_posted:
                item_name = item_posted.item_name
                prefix = (
                    f"{item_name}, created = "
                    if [x for x in _.fk_output_field_specs if x.target == item_name]
                    else ""
                )
                body.abc(f"{item_name}_id = {item_name}_form.pop('id')")
                body.IxI(
                    f"{prefix}{u0(item_name)}.objects.update_or_create",
                    [f"id={item_name}_id", f"defaults={item_name}_form"],
                    "",
                )

            for item_list_deleted in mutation.item_lists_deleted:
                item_name = item_list_deleted.item_name
                body.IxI(
                    f"{u0(item_name)}.objects.filter",
                    [f"id__in={item_name}_ids"],
                    ".delete()",
                )
                body.abc("")

            fk_args = [f"{sn(x.name)}={sn(x.name)}" for x in _.fk_output_field_specs]
            body.IxI(
                f"return {u0(mutation.name)}",
                ["success=True", "errors={}"] + fk_args,
                "",
            )
            return root.result

    return dict(sections=Sections(), _=_)
