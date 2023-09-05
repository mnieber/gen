def get_helpers(_):
    class Helpers:
        use_in_client = _.mutation.api_spec.use_in_client
        input_field_specs = _.mutation.api_spec.get_inputs()
        form_input_field_specs = _.mutation.api_spec.get_inputs(["form"])

        @property
        def form_input_type_specs(self):
            result = []
            for field_spec in self.form_input_field_specs:
                result.append(field_spec.target_type_spec)
            return result

        def split_query_names(self, query_names):
            return [x.split(".") if "." in x else ("api", x) for x in query_names]

    return Helpers()
