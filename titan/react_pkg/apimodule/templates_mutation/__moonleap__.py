from titan.react_pkg.apimodule.graphql_body import graphql_body
from titan.types_pkg.pkg.has_hydrated_fields import has_hydrated_fields


def get_helpers(_):
    class Helpers:
        has_endpoint = "client" in _.mutation.api_spec.has_endpoint
        input_field_specs = _.mutation.api_spec.get_inputs()
        form_input_field_specs = _.mutation.api_spec.get_inputs(["form"])
        fk_output_field_specs = _.mutation.api_spec.get_outputs(["relatedSet", "fk"])
        orders_data = []
        hydrated_fields = []

        def __init__(self):
            self.hydrated_fields = self.get_hydrated_fields()
            self.type_specs_to_import, self.graphql_body = graphql_body(
                _.mutation.api_spec.outputs_type_spec, indent=8
            )

        @property
        def form_input_type_specs(self):
            result = []
            for field_spec in self.form_input_field_specs:
                result.append(field_spec.target_type_spec)
            return result

        def get_hydrated_fields(self):
            result = []
            for field_spec in self.fk_output_field_specs:
                if has_hydrated_fields(field_spec.target_type_spec, "client"):
                    result.append(field_spec)
            return result

    return Helpers()
