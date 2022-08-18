from titan.react_pkg.apimodule.graphql_body import graphql_body


def get_helpers(_):
    class Helpers:
        input_field_specs = _.mutation.gql_spec.get_inputs()
        form_input_field_specs = _.mutation.gql_spec.get_inputs(["form"])
        fk_output_field_specs = _.mutation.gql_spec.get_outputs(["relatedSet", "fk"])

        def graphql_body(self):
            return graphql_body(_.mutation.gql_spec.outputs_type_spec, recurse=True)

        @property
        def form_input_items(self):
            result = []
            for field_spec in self.form_input_field_specs:
                result.append(field_spec.target_item)
            return result

    return Helpers()
