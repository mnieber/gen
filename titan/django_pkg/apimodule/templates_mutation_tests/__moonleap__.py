import os

from moonleap.utils.case import l0, sn
from moonleap.utils.codeblock import CodeBlock
from moonleap.utils.fp import uniq
from titan.django_pkg.djangoapp.define_fixture import create_fixture, define_fixture
from titan.types_pkg.typeregistry import get_type_reg


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

    if t == "uuid[]":
        return r'["41f55a14-a1b7-5697-84ef-c00e3f51c7e2"]'

    if t in ("string", "text"):
        return r'"foo"'

    if t == "url":
        return r'"https://foo.bar.com"'

    if t == "string[]":
        return r'["foo", "bar"]'

    raise Exception(f"Unknown graphene field type: {t} in spec for {field_spec.name}")


def get_helpers(_):
    class Helpers:
        mutation_name = _.mutation.name

        input_field_specs = [
            (x, x.field_type == "form") for x in _.mutation.api_spec.get_inputs()
        ]
        form_input_field_specs = _.mutation.api_spec.get_inputs(["form"])
        id_input_field_specs = _.mutation.api_spec.get_inputs(["uuid", "uuid[]"])
        output_field_specs = _.mutation.api_spec.get_outputs()
        scalar_output_field_specs = [
            x for x in output_field_specs if x.field_type not in ("fk", "relatedSet")
        ]
        fk_output_field_specs = _.mutation.api_spec.get_outputs(["fk"])
        fixtures = [create_fixture(x) for x in id_input_field_specs]
        ids_fixtures = [x for x in fixtures if x.field_spec.field_type == "uuid[]"]
        id_fixtures = [x for x in fixtures if x.field_spec.field_type == "uuid"]

        def mutation_fixture_imports(self):
            result = []

            for form_field_spec in (
                self.form_input_field_specs + self.id_input_field_specs
            ):
                django_module = form_field_spec.target_type_spec.django_module
                if not django_module:
                    continue

                import_path = f"{django_module.module_path}.tests.random_data"
                result.append(
                    f"from {import_path} import create_random_{sn(form_field_spec.target)}"
                )

                for fk_field_spec in _fk_field_specs_for_form_field(form_field_spec):
                    django_module = fk_field_spec.target_type_spec.django_module
                    if not django_module:
                        continue

                    import_path = f"{django_module.module_path}.tests.random_data"
                    result.append(
                        f"from {import_path} import create_random_{sn(l0(fk_field_spec.target))}"
                    )

            return os.linesep.join(uniq(result))

        def define_fixtures(self):
            root = CodeBlock(level=1)

            for fixture in self.fixtures:
                define_fixture(root, fixture)

            return root.result

    return Helpers()


def _fk_field_specs_for_form_field(form_field_spec):
    data_type_spec = get_type_reg().get(form_field_spec.target)
    return data_type_spec.get_field_specs(["fk"])
