import os

import ramda as R
from moonleap.typespec.field_spec import input_is_used_for_output
from moonleap.utils.case import l0, sn
from moonleap.utils.codeblock import CodeBlock
from moonleap.utils.fp import uniq
from moonleap.utils.join import join
from titan.api_pkg.pkg.graphql_args import (
    declare_graphql_variable,
    invoke_graphql_variable,
)
from titan.django_pkg.apiquery.define_fixture import define_fixture


def get_context_test(query, api_module):
    _ = lambda: None
    _.query = query
    _.django_app = api_module.django_app
    _.inputs_type_spec = query.inputs_type_spec
    _.outputs_type_spec = query.outputs_type_spec
    _.input_field_specs = list(_.inputs_type_spec.field_specs)
    _.fk_output_field_specs = _.outputs_type_spec.get_field_specs(["fk", "relatedSet"])

    class Sections:
        def query_fixture_imports(self):
            result = []

            for output_field_spec in _.fk_output_field_specs:
                django_module = output_field_spec.target_django_module(_.django_app)
                result.append(
                    f"from {django_module.module_path}.tests.random_data "
                    f"import create_random_{sn(l0(output_field_spec.target))}"
                )

            return os.linesep.join(uniq(result))

        def define_query_fixtures(self):
            root = CodeBlock(style="python", level=1)

            for output_field_spec in _.fk_output_field_specs:
                define_fixture(root, output_field_spec)

            return root.result

        def invoke_query_fixtures(self):
            result = []
            for output_field_spec in _.fk_output_field_specs:
                fixture = sn(output_field_spec.name)
                result.append(fixture)

            return join(prefix=", ", infix=", ".join(uniq(result)))

        def invoke_create_query_args(self):
            args = []
            for input_field_spec in _.input_field_specs:
                arg_name = sn(input_field_spec.name)
                field_name = sn(input_field_spec.short_name)
                if input_field_spec.related_output:
                    fixture = sn(input_field_spec.related_output)
                    args.append(f"{arg_name}={fixture}.{field_name}")
                else:
                    args.append(f"{arg_name}={arg_name}")

            for output_field_spec in _.fk_output_field_specs:
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

        def declare_create_query_args(self):
            inputs = list(f"{sn(x.name)}" for x in _.input_field_specs)
            outputs = list(
                f"{sn(x.name)}_outputs=None" for x in _.fk_output_field_specs
            )
            return ", ".join(inputs + outputs)

        def declare_graphql_query_args(self):
            endpoint_args = [
                f'"{declare_graphql_variable(x)}"' for x in _.input_field_specs
            ]
            return ", ".join(endpoint_args)

        def invoke_query_endpoint(self, output_field_spec):
            endpoint_args = [
                f'"{invoke_graphql_variable(x)}"'
                for x in _.input_field_specs
                if input_is_used_for_output(x, output_field_spec)
            ]
            return ", ".join(endpoint_args)

        def query_variables(self):
            args = ", ".join([f"{x.name}={sn(x.name)}" for x in _.input_field_specs])
            return f"dict({args})"

    return dict(sections=Sections(), _=_)
