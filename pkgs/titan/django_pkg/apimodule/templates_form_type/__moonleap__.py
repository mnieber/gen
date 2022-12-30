def get_helpers(_):
    class Helpers:
        field_specs = _.form_type_spec.get_field_specs()

        def args(self, field_spec):
            return "required=False" if field_spec.is_optional("server") else ""

    return Helpers()
