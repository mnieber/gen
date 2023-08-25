def get_helpers(_):
    class Helpers:
        field_specs = [x for x in _.form_type_spec.get_field_specs() if x.has_api]

        def args(self, field_spec):
            return "" if field_spec.is_optional else "required=True"

    return Helpers()
