from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec

from .utils import (
    get_output_field_name_for_named_item,
    get_output_field_name_for_named_item_list,
)


def get_default_outputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            *[
                _item_output_field_spec(self, named_item)
                for named_item in self.named_items_provided
            ],
            *[
                _item_list_output_field_spec(self, named_item_list)
                for named_item_list in self.named_item_lists_provided
            ],
        ],
    )


def _item_output_field_spec(self, named_item):
    item_name, output_field_name = get_output_field_name_for_named_item(named_item)
    return FieldSpec(
        name=output_field_name,
        required=False,
        private=False,
        field_type="fk",
        field_type_attrs=dict(
            target=item_name,
            hasRelatedSet=False,
        ),
    )


def _item_list_output_field_spec(self, named_item_list):
    item_name, output_field_name = get_output_field_name_for_named_item_list(
        named_item_list
    )
    return FieldSpec(
        name=output_field_name,
        required=False,
        private=False,
        field_type="relatedSet",
        field_type_attrs=dict(target=item_name),
    )
