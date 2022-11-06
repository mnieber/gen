from moonleap.utils.fp import append_uniq, uniq


def get_helpers(_):
    class Helpers:
        input_field_specs = _.mutation.gql_spec.get_inputs()
        fk_input_field_specs = _.mutation.gql_spec.get_inputs(["fk", "relatedSet"])
        output_field_specs = _.mutation.gql_spec.get_outputs()
        fk_output_field_specs = _.mutation.gql_spec.get_outputs(["fk", "relatedSet"])

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
        def items_to_import(self):
            result = []
            for field_spec in self.fk_input_field_specs + self.fk_output_field_specs:
                append_uniq(result, field_spec.target_item)

            for item in self.items_saved:
                append_uniq(result, item)

            for item in self.items_deleted:
                append_uniq(result, item)

            return result

        def graphene_type(self, field_spec):
            return field_spec.graphene_type(
                "required=False" if field_spec.is_optional("server") else ""
            )

    return Helpers()
