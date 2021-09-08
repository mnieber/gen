import ramda as R
from moonleap import upper0
from moonleap.resources.data_type_spec_store import (
    DataTypeField,
    DataTypeSpec,
    data_type_spec_store,
)
from moonleap.utils.inflect import plural


def provides_item(self, item_name):
    return [x for x in self.items_provided if x.item_name == item_name]


def provides_item_list(self, item_name):
    return [x for x in self.item_lists_provided if x.item_name == item_name]


def _item_field(self, item):
    return (
        DataTypeField(
            name_snake=item.name_snake,
            name=item.name,
            required=False,
            private=False,
            field_type="fk",
            field_type_attrs=dict(target=upper0(item.item_name), has_related_set=False),
        ),
    )


def _item_list_field(self, item):
    return (
        DataTypeField(
            name_snake=plural(item.name_snake),
            name=plural(item.name),
            required=False,
            private=False,
            field_type="fk",
            field_type_attrs=dict(target=upper0(item.item_name), has_related_set=False),
        ),
    )


def data_type_out(self):
    name = f"{self.name}OutputType"
    spec = data_type_spec_store.spec_by_name.get(name)
    if spec:
        return spec

    return DataTypeSpec(
        type_name=name,
        field_by_name=R.index_by(
            R.prop("name"),
            [
                *[_item_field(self, item) for item in self.items_provided],
                *[
                    _item_list_field(self, item_list)
                    for item_list in self.item_lists_provided
                ],
            ],
        ),
    )
