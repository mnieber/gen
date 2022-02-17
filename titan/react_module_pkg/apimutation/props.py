import os
from pathlib import Path

import ramda as R
from moonleap import render_templates
from moonleap.utils.case import l0
from titan.api_pkg.pkg.graphql_args import graphql_args
from titan.react_module_pkg.apiquery.graphql_body import graphql_body
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type


def get_context(mutation, api_module):
    _ = lambda: None
    _.api_module = api_module
    _.mutation = mutation
    _.input_field_specs = mutation.inputs_type_spec.field_specs
    _.form_input_field_specs = [
        x for x in _.input_field_specs if x.field_type == "form"
    ]
    _.output_schema_name = mutation.name + "Outputs"
    _.fk_output_field_specs = mutation.outputs_type_spec.get_field_specs(
        ["relatedSet", "fk"]
    )

    class Sections:
        def ts_type_imports(self):
            result = []
            for field_spec in _.form_input_field_specs:
                item_name = l0(field_spec.target)
                item = _.api_module.graphql_api.type_reg.get_item_by_name(item_name)
                result.append(
                    f"import {{ {item.item_type.ts_form_type} }} "
                    + f"from '{item.item_type.ts_type_import_path}';"
                )
            return os.linesep.join(result)

        def ts_mutation_args(self):
            return ", ".join(
                R.map(
                    lambda field_spec: f"{field_spec.name}: "
                    + f"{field_spec_to_ts_type(field_spec, fk_as_str=False)}",
                    _.input_field_specs,
                )
            )

        def ts_mutation_graphql_args(self, before):
            return graphql_args(_.input_field_specs, before)

        def ts_mutation_graphql_body(self):
            return graphql_body(_.mutation.outputs_type_spec, recurse=False)

        def ts_mutation_graphql_variables(self):
            tab = " " * 6
            return tab + ("," + os.linesep + tab).join(
                [field_spec.name for field_spec in _.input_field_specs]
            )

        def invalidate_queries(self):
            query_names = set()

            for item_list in mutation.item_lists_deleted:
                for query in mutation.graphql_api.queries:
                    for named_item in query.named_items_provided:
                        if named_item.typ.item_name == item_list.item_name:
                            query_names.add(query.name)

            result = ""
            for query_name in query_names:
                result += f'    queryClient.invalidateQueries("{query_name}");\n'
            return result

    return dict(sections=Sections(), _=_)


def render_mutation_endpoint(api_module, mutation, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        mutation, write_file, render_template, output_path=api_module.merged_output_path
    )
