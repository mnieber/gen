def get_helpers(_):
    class Helpers:
        has_endpoint = _.query.api_spec.has_endpoint
        input_field_specs = _.query.api_spec.get_inputs()

    return Helpers()
