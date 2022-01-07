import ramda as R
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec
from moonleap.utils.case import camel_join
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name

from .utils import (
    get_output_field_name_for_named_item,
    get_output_field_name_for_named_item_list,
)


def _input_field_spec(field_type, field_name, related_output):
    return FieldSpec(
        name=field_name,
        required=False,
        private=False,
        field_type=field_type,
        field_type_attrs=dict(related_output=related_output),
    )


def get_default_inputs_type_spec(self, name):
    input_field_specs = []

    def maybe_create_input_field_specs(src_type_spec, related_output, is_fk):
        query_by = (
            src_type_spec.query_item_by if is_fk else src_type_spec.query_items_by
        )
        for src_field_name in query_by or []:
            input_field_name = camel_join(related_output, src_field_name)
            if not R.head(x for x in input_field_specs if x.name == input_field_name):
                input_field_specs.append(
                    _input_field_spec(
                        src_type_spec.get_field_spec_by_name(src_field_name).field_type,
                        input_field_name,
                        related_output,
                    )
                )

    for named_item_provided in self.named_items_provided:
        item_name, output_field_name = get_output_field_name_for_named_item(
            named_item_provided
        )
        maybe_create_input_field_specs(
            src_type_spec=ml_type_spec_from_item_name(item_name),
            related_output=output_field_name,
            is_fk=True,
        )

    for named_item_list_provided in self.named_item_lists_provided:
        item_name, output_field_name = get_output_field_name_for_named_item_list(
            named_item_list_provided
        )
        maybe_create_input_field_specs(
            src_type_spec=ml_type_spec_from_item_name(item_name),
            related_output=output_field_name,
            is_fk=False,
        )

    return TypeSpec(type_name=name, field_specs=input_field_specs)
