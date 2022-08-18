from titan.react_pkg.apimodule.graphql_body import graphql_body


def get_helpers(_):
    class Helpers:
        input_field_specs = _.query.gql_spec.get_inputs()
        output_schema_name = _.query.name + "Outputs"
        fk_output_field_specs = _.query.gql_spec.get_outputs(["relatedSet", "fk"])
        scalar_output_field_specs = [
            x
            for x in _.query.gql_spec.get_outputs()
            if x.field_type not in ["relatedSet", "fk"]
        ]

        def ts_graphql_query_body(self, output_field_spec):
            return graphql_body(output_field_spec.target_type_spec)

    return Helpers()
