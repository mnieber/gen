import os

from moonleap.typespec.type_spec_store import type_spec_store
from moonleap.utils.case import l0, sn
from moonleap.utils.codeblock import CodeBlock
from moonleap.utils.fp import uniq
from titan.django_pkg.djangoapp.define_fixture import define_fixture


def field_spec_default_value(field_spec):
    t = field_spec.field_type

    if t == "fk":
        return f"{sn(field_spec.name)}.id"

    if t == "boolean":
        return r"True"

    if t == "int":
        return r"123"

    if t == "float":
        return r"1.23"

    if t == "date":
        return r'"01-02-2003"'

    if t == "email":
        return r"email@email.com"

    if t == "slug":
        return r'"foo-bar"'

    if t == "uuid":
        return r'"41f55a14-a1b7-5697-84ef-c00e3f51c7e2"'

    if t in ("string", "text"):
        return r'"foo"'

    if t == "url":
        return r'"https://foo.bar.com"'

    if t == "idList":
        return r"[]"

    raise Exception(f"Unknown graphene field type: {t} in spec for {field_spec.name}")


def _get_fixture_field_specs(form_input_field_specs):
    result = []
    for input_field_spec in form_input_field_specs:
        type_spec = type_spec_store().get(input_field_spec.target)
        for fk_field_spec in type_spec.get_field_specs(["fk"]):
            if fk_field_spec not in result:
                result.append(fk_field_spec)

    return result


def fk_field_specs_for_form_field(form_field_spec):
    data_type_spec = type_spec_store().get(form_field_spec.target)
    return data_type_spec.get_field_specs(["fk"])


def get_helpers(_):
    class Helpers:
        input_field_specs = list(_.mutation.gql_spec.get_inputs())
        form_input_field_specs = _.mutation.gql_spec.get_inputs(["form"])
        output_field_specs = _.mutation.gql_spec.get_outputs()
        fk_output_field_specs = _.mutation.gql_spec.get_outputs(["fk"])
        fixture_field_specs = _get_fixture_field_specs(form_input_field_specs)

        def mutation_fixture_imports(self):
            result = []

            for form_field_spec in self.form_input_field_specs:
                django_module = form_field_spec.target_item.django_module
                if not django_module:
                    continue

                import_path = f"{django_module.module_path}.tests.random_data"
                form_type_name = form_field_spec.target + "Form"
                result.append(
                    f"from {import_path} import create_random_{sn(form_type_name)}"
                )

                for fk_field_spec in fk_field_specs_for_form_field(form_field_spec):
                    django_module = fk_field_spec.target_item.django_module
                    if not django_module:
                        continue

                    import_path = f"{django_module.module_path}.tests.random_data"
                    result.append(
                        f"from {import_path} import create_random_{sn(l0(fk_field_spec.target))}"
                    )

            return os.linesep.join(uniq(result))

        def define_fixtures(self):
            root = CodeBlock(style="python", level=1)

            for field_spec in self.fixture_field_specs:
                define_fixture(root, field_spec)

            return root.result

        def create_mutation_args(self):
            root = CodeBlock(style="python", level=1)

            for input_field_spec in self.input_field_specs:
                input_arg_name = sn(input_field_spec.name)

                if input_field_spec.field_type == "form":
                    create_form_args = []
                    for fk_field_spec in fk_field_specs_for_form_field(
                        input_field_spec
                    ):
                        arg_name = sn(fk_field_spec.name + "Id")
                        fixture = sn(fk_field_spec.name)
                        create_form_args.append(f"{arg_name}={fixture + '.id'}")

                    form_type_name = l0(input_field_spec.target) + "Form"
                    root.IxI(
                        f"{input_arg_name}=create_random_{sn(form_type_name)}",
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
                    for x in self.output_field_specs
                    if x.field_type not in ("fk", "relatedSet")
                ],
                "]",
            )
            return root.result

    return Helpers()
