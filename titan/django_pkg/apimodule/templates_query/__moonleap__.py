from moonleap.utils.fp import append_uniq


def get_helpers(_):
    class Helpers:
        input_field_specs = list(_.query.gql_spec.get_inputs())
        output_field_specs = list(_.query.gql_spec.get_outputs())

        @property
        def items_to_import(self):
            result = []
            for field_spec in _.query.gql_spec.get_outputs(
                ["fk", "relatedSet", "idList"]
            ):
                append_uniq(result, field_spec.target_item)

            return result

    return Helpers()
