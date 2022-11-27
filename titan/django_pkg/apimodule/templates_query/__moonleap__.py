from moonleap.utils.fp import append_uniq


def get_helpers(_):
    class Helpers:
        input_field_specs = list(_.query.api_spec.get_inputs())
        output_field_specs = list(_.query.api_spec.get_outputs())

        @property
        def type_specs_to_import(self):
            result = []
            for field_spec in _.query.api_spec.get_outputs(["fk", "relatedSet"]):
                append_uniq(result, field_spec.target_type_spec)

            return result

    return Helpers()
