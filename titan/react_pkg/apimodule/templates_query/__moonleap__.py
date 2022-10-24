from moonleap.typespec.has_derived_fields import has_derived_fields
from titan.react_pkg.apimodule.graphql_body import graphql_body


def get_helpers(_):
    class Helpers:
        input_field_specs = _.query.gql_spec.get_inputs()
        output_schema_name = _.query.name + "Outputs"
        fk_output_field_specs = _.query.gql_spec.get_outputs(["relatedSet", "fk"])
        scalar_output_field_specs = [
            x
            for x in _.query.gql_spec.get_outputs()
            if x.field_type not in ["relatedSet", "fk"] and "client" in x.has_api
        ]

        def __init__(self):
            self.derived_fields = self.get_derived_fields()
            self.type_specs_to_import, self.graphql_body = graphql_body(
                _.query.gql_spec.outputs_type_spec, indent=8
            )

        def get_derived_fields(self):
            result = []
            for field_spec in self.fk_output_field_specs:
                if has_derived_fields(field_spec.target_type_spec, "client"):
                    result.append(field_spec)
            return result

    return Helpers()
