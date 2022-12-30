import os

from moonleap.utils.case import l0, sn
from moonleap.utils.codeblock import CodeBlock
from moonleap.utils.fp import uniq
from titan.django_pkg.djangoapp.define_fixture import define_fixture


def get_helpers(_):
    class Helpers:
        input_field_specs = list(_.query.api_spec.get_inputs())
        output_field_specs = list(_.query.api_spec.get_outputs())
        fk_output_field_specs = list(_.query.api_spec.get_outputs(["fk", "relatedSet"]))

        def query_fixture_imports(self):
            result = []

            for output_field_spec in self.fk_output_field_specs:
                django_module = output_field_spec.target_type_spec.django_module
                result.append(
                    f"from {django_module.module_path}.tests.random_data "
                    f"import create_random_{sn(l0(output_field_spec.target))}"
                )

            return os.linesep.join(uniq(result))

        def define_query_fixtures(self):
            root = CodeBlock(style="python", level=1)

            for output_field_spec in self.fk_output_field_specs:
                define_fixture(root, output_field_spec)

            return root.result

        def invoke_create_query_args(self):
            args = []
            for input_field_spec in self.input_field_specs:
                arg_name = sn(input_field_spec.name)
                args.append(f"{arg_name}={arg_name}")

            for output_field_spec in self.fk_output_field_specs:
                args.append(f"{sn(output_field_spec.name)}_outputs=['id']")

            return ", ".join(args)

        def assert_query_response(self, output_field_spec):
            root = CodeBlock(style="python", level=2)
            if output_field_spec.field_type == "fk":
                root.abc(f"assert data['{output_field_spec.name}'] == {{")
                root.abc(f"  'id': {sn(output_field_spec.name)}.id")
                root.abc(r"}")
            elif output_field_spec.field_type == "relatedSet":
                root.abc(f"assert len(data['{output_field_spec.name}'])")
            else:
                root.abc(f"assert data['{output_field_spec.name}']" + f" != None")

            return root.result

    return Helpers()
