from moonleap.utils.fp import add_to_list_as_set


def get_helpers(_):
    class Helpers:
        inputs_type_spec = _.mutation.inputs_type_spec
        outputs_type_spec = _.mutation.outputs_type_spec
        input_field_specs = list(inputs_type_spec.field_specs)
        output_field_specs = list(outputs_type_spec.field_specs)
        fk_output_field_specs = outputs_type_spec.get_field_specs(["fk"])

        @property
        def item_types_to_import(self):
            result = []
            for type_spec in [self.inputs_type_spec, self.outputs_type_spec]:
                for field_spec in type_spec.get_field_specs(
                    ["fk", "relatedSet", "form", "idList"]
                ):
                    add_to_list_as_set(result, field_spec.target_item_type)

            return result

        def graphene_output_type(self, field_spec):
            return field_spec.graphene_output_type(f"required={field_spec.required}")

    return Helpers()
