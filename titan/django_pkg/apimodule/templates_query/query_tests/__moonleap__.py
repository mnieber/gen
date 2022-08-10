import os

from moonleap.typespec.field_spec import input_is_used_for_output
from moonleap.utils.case import l0, sn
from moonleap.utils.codeblock import CodeBlock
from moonleap.utils.fp import uniq
from titan.django_pkg.djangoapp.define_fixture import define_fixture


def get_helpers(_):
    class Helpers:
        inputs_type_spec = _.query.inputs_type_spec
        outputs_type_spec = _.query.outputs_type_spec
        input_field_specs = list(inputs_type_spec.field_specs)
        output_field_specs = list(outputs_type_spec.field_specs)
        fk_output_field_specs = outputs_type_spec.get_field_specs(["fk", "relatedSet"])

        def query_fixture_imports(self):
            result = []

            for output_field_spec in self.fk_output_field_specs:
                django_module = output_field_spec.target_item_type.django_module
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
                field_name = sn(input_field_spec.short_name)
                if input_field_spec.related_output:
                    fixture = sn(input_field_spec.related_output)
                    args.append(f"{arg_name}={fixture}.{field_name}")
                else:
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

        def invoke_query_endpoint(self, output_field_spec):
            endpoint_args = [
                f"{x.short_name}: ${x.name}"
                for x in self.input_field_specs
                if input_is_used_for_output(x, output_field_spec)
            ]
            return ", ".join(endpoint_args)

    return Helpers()
