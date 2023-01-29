def get_helpers(_):
    class Helpers:
        field_specs = [
            x for x in _.form_type_spec.get_field_specs() if "server" in x.has_api
        ]

        def args(self, field_spec):
            return "required=False" if field_spec.is_optional("server") else ""

    return Helpers()
