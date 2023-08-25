def get_helpers(_):
    class Helpers:
        field_specs = sorted(
            [x for x in _.form_type_spec.get_field_specs() if x.has_api],
            key=lambda x: x.name,
        )

        def args(self, field_spec):
            return "" if field_spec.is_optional else "required=True"

    return Helpers()
