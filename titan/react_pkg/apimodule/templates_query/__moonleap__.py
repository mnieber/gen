from titan.react_pkg.apimodule.graphql_body import graphql_body


def get_helpers(_):
    class Helpers:
        input_field_specs = _.query.inputs_type_spec.field_specs
        output_schema_name = _.query.name + "Outputs"
        fk_output_field_specs = _.query.outputs_type_spec.get_field_specs(
            ["relatedSet", "fk"]
        )

        def ts_graphql_query_body(self, output_field_spec):
            return graphql_body(output_field_spec.target_type_spec)

    return Helpers()
