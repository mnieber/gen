from moonleap.typespec.field_spec import FkFieldSpec
from moonleap.typespec.type_spec_store import TypeSpec


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
    return FkFieldSpec(
        name=named_item.output_field_name,
        required=False,
        private=False,
        field_type="fk",
        field_type_attrs=dict(
            target=named_item.typ.item_type.name,
            hasRelatedSet=False,
        ),
    )


def _item_list_output_field_spec(self, named_item_list):
    return FkFieldSpec(
        name=named_item_list.output_field_name,
        required=False,
        private=False,
        field_type="relatedSet",
        field_type_attrs=dict(target=named_item_list.typ.item_type.name),
    )
