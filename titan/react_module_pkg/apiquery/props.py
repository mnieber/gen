import os
from pathlib import Path

import ramda as R
from moonleap import render_templates
from titan.api_pkg.pkg.graphql_args import graphql_args
from titan.react_module_pkg.apiquery.graphql_body import graphql_body
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type


def define_schema_field(field_spec, output_schema_name):
    output_many = field_spec.field_type in ("relatedSet",)
    fk_item_name = field_spec.target
    value = f"[{fk_item_name}]" if output_many else fk_item_name
    line = f"{output_schema_name}.define({{ {field_spec.name}: {value} }});"
    return line


def get_context(query, api_module):
    _ = lambda: None
    _.api_module = api_module
    _.query = query
    _.input_field_specs = query.inputs_type_spec.field_specs
    _.output_schema_name = query.name + "Outputs"
    _.fk_output_field_specs = query.outputs_type_spec.get_field_specs(
        ["relatedSet", "fk"]
    )

    class Sections:
        def schema_imports(self):
            result = []
            for field_spec in _.fk_output_field_specs:
                fk_item_name = field_spec.target
                result.append(f"import {{ {fk_item_name} }} from 'src/api/schema';")

            return os.linesep.join(result)

        def query_output_schema_fields(self):
            result = []
            for field_spec in _.fk_output_field_specs:
                result.append(define_schema_field(field_spec, _.output_schema_name))
            return os.linesep.join(result)

        def javascript_args(self):
            return ", ".join(
                R.map(
                    lambda field_spec: f"{field_spec.name}: "
                    + f"{field_spec_to_ts_type(field_spec, fk_as_str=False)}",
                    _.input_field_specs,
                )
            )

        def ts_graphql_query_args(self, before):
            return graphql_args(_.input_field_specs, before)

        def ts_graphql_query_body(self, output_field_spec):
            if output_field_spec.field_type in ("fk", "relatedSet"):
                return graphql_body(output_field_spec.target_type_spec)
            else:
                raise Exception(
                    f"Not implemented: graphql_body for field {output_field_spec.name}"
                )

        def graphql_variables(self):
            tab = " " * 6
            return tab + ("," + os.linesep + tab).join(
                [field_spec.name for field_spec in _.input_field_specs]
            )

    return dict(sections=Sections(), _=_)


def render_query_endpoint(api_module, query, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        query, write_file, render_template, output_path=api_module.merged_output_path
    )
