import os

import ramda as R
from moonleap.utils.case import sn
from moonleap.utils.codeblock import CodeBlock
from moonleap.utils.join import join
from titan.api_pkg.pkg.graphql_args import declare_graphql_variable
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name
from titan.django_pkg.apiquery.get_context_test import define_fixture
from titan.django_pkg.graphene_django.utils import find_module_that_provides_item_list
from titan.django_pkg.pkg.field_spec_default_value import field_spec_default_value


def _get_fixture_field_specs(form_input_field_specs):
    result = []
    for input_field_spec in form_input_field_specs:
        type_spec = ml_type_spec_from_item_name(input_field_spec.target)
        for fk_field_spec in type_spec.get_field_specs(["fk"]):
            if fk_field_spec not in result:
                result.append(fk_field_spec)

    return result


def fk_field_specs_for_form_field(form_field_spec):
    data_type_spec = ml_type_spec_from_item_name(form_field_spec.target)
    return data_type_spec.get_field_specs(["fk"])


def get_context_test(mutation, api_module):
    _ = lambda: None
    _.mutation = mutation
    _.django_app = api_module.django_app
    _.inputs_type_spec = mutation.inputs_type_spec
    _.outputs_type_spec = mutation.outputs_type_spec
    _.input_field_specs = list(_.inputs_type_spec.field_specs)
    _.form_input_field_specs = _.inputs_type_spec.get_field_specs(["form"])
    _.output_field_specs = list(_.outputs_type_spec.field_specs)
    _.fk_output_field_specs = _.outputs_type_spec.get_field_specs(["fk"])
    _.fixture_field_specs = _get_fixture_field_specs(_.form_input_field_specs)

    class Sections:
        def mutation_fixture_imports(self):
            result = []

            for form_field_spec in _.form_input_field_specs:
                django_module = find_module_that_provides_item_list(
                    _.django_app, form_field_spec.target
                )
                import_path = f"{django_module.module_path}.tests.random_data"
                form_item_name = form_field_spec.target + "Form"
                result.append(
                    f"from {import_path} import create_random_{sn(form_item_name)}"
                )

                for fk_field_spec in fk_field_specs_for_form_field(form_field_spec):
                    django_module = find_module_that_provides_item_list(
                        _.django_app, fk_field_spec.target
                    )
                    import_path = f"{django_module.module_path}.tests.random_data"
                    item_name = fk_field_spec.target
                    result.append(
                        f"from {import_path} import create_random_{sn(item_name)}"
                    )

            return os.linesep.join(R.uniq(result))

        def define_fixtures(self):
            root = CodeBlock(style="python", level=1)

            for field_spec in _.fixture_field_specs:
                define_fixture(root, field_spec)

            return root.result

        def create_mutation_args(self):
            root = CodeBlock(style="python", level=1)

            for input_field_spec in _.input_field_specs:
                input_arg_name = sn(input_field_spec.name)

                if input_field_spec.field_type == "form":
                    create_form_args = []
                    for fk_field_spec in fk_field_specs_for_form_field(
                        input_field_spec
                    ):
                        arg_name = sn(fk_field_spec.name + "Id")
                        fixture = sn(fk_field_spec.name)
                        create_form_args.append(f"{arg_name}={fixture + '.id'}")

                    form_item_name = input_field_spec.target + "Form"
                    root.IxI(
                        f"{input_arg_name}=create_random_{sn(form_item_name)}",
                        create_form_args,
                        ",",
                    )
                else:
                    value = field_spec_default_value(input_field_spec)
                    root.abc(f"{input_arg_name}={value}, ")

            root._x_(
                f"output_values=[",
                [
                    f"'{x.name}'"
                    for x in _.output_field_specs
                    if x.field_type not in ("fk", "relatedSet")
                ],
                "]",
            )
            return root.result

        def invoke_mutation_fixtures(self):
            result = []
            for output_field_spec in _.fixture_field_specs:
                result.append(sn(output_field_spec.name))
            return join(prefix=", ", infix=", ".join(R.uniq(result)))

        def declare_create_mutation_args(self):
            inputs = list(f"{sn(x.name)}" for x in _.input_field_specs)
            outputs = list(
                f"{sn(x.name)}_outputs=None" for x in _.fk_output_field_specs
            )
            outputs += ["output_values=None"]

            return ", ".join(inputs + outputs)

        def declare_graphql_mutation_args(self):
            endpoint_args = [
                f'"{declare_graphql_variable(x)}"' for x in _.input_field_specs
            ]
            return ", ".join(endpoint_args)

        def invoke_mutation_endpoint(self):
            inputs = list(f'"{x.name}: ${x.name}"' for x in _.input_field_specs)
            return ", ".join(inputs)

        def mutation_variables(self):
            inputs = list(f"{x.name}={sn(x.name)}" for x in _.input_field_specs)
            return ", ".join(inputs)

    return dict(sections=Sections(), _=_)
