from moonleap.typespec.field_spec import input_is_used_for_output
from moonleap.utils.case import sn
from moonleap.utils.fp import add_to_list_as_set


def get_helpers(_):
    class Helpers:
        inputs_type_spec = _.query.inputs_type_spec
        outputs_type_spec = _.query.outputs_type_spec
        input_field_specs = list(inputs_type_spec.field_specs)
        output_field_specs = list(outputs_type_spec.field_specs)

        @property
        def item_types_to_import(self):
            result = []
            for type_spec in [self.outputs_type_spec]:
                for field_spec in type_spec.get_field_specs(
                    ["fk", "relatedSet", "form", "idList"]
                ):
                    add_to_list_as_set(result, field_spec.target_item_type)

            return result

        def graphene_output_type(self, output_field_spec):
            return output_field_spec.graphene_output_type(
                ", ".join(
                    f"{sn(input_field_spec.short_name)}={input_field_spec.graphene_input_type}"
                    for input_field_spec in self.input_field_specs
                    if input_is_used_for_output(input_field_spec, output_field_spec)
                )
            )

    return Helpers()
