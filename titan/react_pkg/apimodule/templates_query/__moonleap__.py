from titan.react_pkg.apimodule.graphql_body import graphql_body
from titan.types_pkg.pkg.has_hydrated_fields import has_hydrated_fields


def get_helpers(_):
    class Helpers:
        input_field_specs = _.query.gql_spec.get_inputs()
        output_schema_name = _.query.name + "Outputs"
        fk_output_field_specs = _.query.gql_spec.get_outputs(["relatedSet", "fk"])

        def __init__(self):
            self.hydrated_fields = self.get_hydrated_fields()
            self.type_specs_to_import, self.graphql_body = graphql_body(
                _.query.gql_spec.outputs_type_spec, indent=8
            )

        def get_hydrated_fields(self):
            result = []
            for field_spec in self.fk_output_field_specs:
                if has_hydrated_fields(field_spec.target_type_spec, "client"):
                    result.append(field_spec)
            return result

    return Helpers()
