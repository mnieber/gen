import ramda as R
from moonleap import upper0
from moonleap.resources.type_spec_store import FieldSpec, TypeSpec, type_spec_store
from moonleap.utils.inflect import plural


def _default_inputs_type_spec(self, name):
    if self.items_provided and not self.item_lists_provided:
        return TypeSpec(
            type_name=name,
            field_spec_by_name=R.index_by(
                R.prop("name"),
                [
                    FieldSpec(
                        name_snake="id",
                        name="id",
                        required=False,
                        private=False,
                        field_type="string",
                    )
                ],
            ),
        )
    else:
        return TypeSpec(
            type_name=name,
            field_spec_by_name={},
        )


def _default_outputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_spec_by_name=R.index_by(
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


def provides_item(self, item_name):
    return [x for x in self.items_provided if x.item_name == item_name]


def provides_item_list(self, item_name):
    return [x for x in self.item_lists_provided if x.item_name == item_name]


def _item_field(self, item):
    return FieldSpec(
        name_snake=item.item_name_snake,
        name=item.item_name,
        required=False,
        private=False,
        field_type="fk",
        field_type_attrs=dict(target=upper0(item.item_name), has_related_set=False),
    )


def _item_list_field(self, item):
    return FieldSpec(
        name_snake=plural(item.item_name_snake),
        name=plural(item.item_name),
        required=False,
        private=False,
        field_type="fk",
        field_type_attrs=dict(target=upper0(item.item_name), has_related_set=False),
    )


def inputs_type_spec(self):
    name = f"{self.name}InputType"
    return type_spec_store.get(name) or _default_inputs_type_spec(name)


def outputs_type_spec(self):
    name = f"{self.name}OutputType"
    return type_spec_store.get(name) or _default_outputs_type_spec(self, name)
