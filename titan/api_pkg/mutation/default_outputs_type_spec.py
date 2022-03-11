from moonleap.typespec.field_spec import FieldSpec, FkFieldSpec
from moonleap.typespec.type_spec_store import TypeSpec
from moonleap.utils.case import camel_join
from moonleap.utils.inflect import plural


def default_outputs_type_spec(self, name):
    fk_field_specs = [
        FkFieldSpec(
            name=camel_join(named_item.name, named_item.typ.item_name),
            required=False,
            private=False,
            field_type="fk",
            field_type_attrs=dict(target=named_item.typ.item_type.name),
        )
        for named_item in self.named_items_returned
    ]
    related_set_field_specs = [
        FkFieldSpec(
            name=camel_join(
                named_item_list.name, plural(named_item_list.typ.item_name)
            ),
            required=False,
            private=False,
            field_type="relatedSet",
            field_type_attrs=dict(target=named_item_list.typ.item_type.name),
        )
        for named_item_list in self.named_item_lists_returned
    ]
    return TypeSpec(
        type_name=name,
        field_specs=[
            *fk_field_specs,
            *related_set_field_specs,
            FieldSpec(
                name="success",
                required=False,
                private=False,
                field_type="boolean",
            ),
            FieldSpec(
                name="errors",
                required=False,
                private=False,
                field_type="any",
            ),
        ],
    )
