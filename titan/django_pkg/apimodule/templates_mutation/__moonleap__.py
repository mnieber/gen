from moonleap.utils.fp import append_uniq, uniq


def get_helpers(_):
    class Helpers:
        input_field_specs = _.mutation.api_spec.get_inputs()
        optional_input_field_specs = [
            x for x in input_field_specs if x.is_optional("server")
        ]
        required_input_field_specs = [
            x for x in input_field_specs if not x.is_optional("server")
        ]
        fk_input_field_specs = _.mutation.api_spec.get_inputs(["fk", "relatedSet"])
        output_field_specs = _.mutation.api_spec.get_outputs()
        fk_output_field_specs = _.mutation.api_spec.get_outputs(["fk", "relatedSet"])

        @property
        def items_deleted(self):
            return uniq(
                list(_.mutation.items_deleted)
                + [x.item for x in _.mutation.item_lists_deleted]
            )

        @property
        def items_saved(self):
            return uniq(
                list(_.mutation.items_saved)
                + [x.item for x in _.mutation.item_lists_saved]
            )

        @property
        def type_specs_to_import(self):
            result = []
            for field_spec in self.fk_input_field_specs + self.fk_output_field_specs:
                append_uniq(result, field_spec.target_type_spec)

            for item in self.items_saved:
                append_uniq(result, item.type_spec)

            for item in self.items_deleted:
                append_uniq(result, item.type_spec)

            return result

        def graphene_type(self, field_spec):
            return field_spec.graphene_type(
                "" if field_spec.is_optional("server") else "required=True"
            )

    return Helpers()
