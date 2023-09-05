def get_helpers(_):
    class Helpers:
        use_in_client = _.query.api_spec.use_in_client
        input_field_specs = _.query.api_spec.get_inputs()

    return Helpers()
