def get_helpers(_):
    class Helpers:
        has_endpoint = _.mutation.api_spec.has_endpoint
        input_field_specs = _.mutation.api_spec.get_inputs()
        form_input_field_specs = _.mutation.api_spec.get_inputs(["form"])

        @property
        def form_input_type_specs(self):
            result = []
            for field_spec in self.form_input_field_specs:
                result.append(field_spec.target_type_spec)
            return result

    return Helpers()
