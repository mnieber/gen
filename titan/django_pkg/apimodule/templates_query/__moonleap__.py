from moonleap.utils.fp import append_uniq


def get_helpers(_):
    class Helpers:
        input_field_specs = sorted(
            list(_.query.api_spec.get_inputs()), key=lambda x: x.name
        )
        output_field_specs = sorted(
            list(_.query.api_spec.get_outputs()), key=lambda x: x.name
        )
        required_input_field_specs = [
            x for x in input_field_specs if not x.is_optional("server")
        ]
        optional_input_field_specs = [
            x for x in input_field_specs if x.is_optional("server")
        ]

        @property
        def type_specs_to_import(self):
            result = []
            for field_spec in _.query.api_spec.get_outputs(["fk", "relatedSet"]):
                append_uniq(result, field_spec.target_type_spec)

            return result

    return Helpers()
