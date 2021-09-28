from moonleap import u0
from moonleap.resources.field_spec import FieldSpec
from moonleap.resources.type_spec_store import TypeSpec, type_spec_store
from moonleap.utils.inflect import plural


def _default_inputs_type_spec(self, name):
    if self.items_provided and not self.item_lists_provided:
        return TypeSpec(
            type_name=name,
            field_specs=[
                FieldSpec(
                    name_snake="id",
                    name="id",
                    required=False,
                    private=False,
                    field_type="uuid",
                )
            ],
        )
    else:
        return TypeSpec(type_name=name, field_specs=[])


def _default_outputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            *[_item_field(self, item) for item in self.items_provided],
            *[
                _item_list_field(self, item_list)
                for item_list in self.item_lists_provided
            ],
        ],
    )


def provides_item(self, item_name):
    return [x for x in self.items_provided if x.item_name == item_name]


def provides_item_list(self, item_name):
    return [x for x in self.item_lists_provided if x.item_name == item_name]


def _item_field(self, item):
    return FieldSpec(
        name_snake=f"{item.item_name_snake}",
        name=f"{item.item_name}",
        required=False,
        private=False,
        field_type="fk",
        field_type_attrs=dict(
            target=item.item_name,
            has_related_set=False,
        ),
    )


def _item_list_field(self, item):
    return FieldSpec(
        name_snake=f"{plural(item.item_name_snake)}",
        name=f"{plural(item.item_name)}",
        required=False,
        private=False,
        field_type="related_set",
        field_type_attrs=dict(target=item.item_name),
    )


def inputs_type_spec(self):
    spec_name = f"{u0(self.name)}Input"
    if not type_spec_store().has(spec_name):
        type_spec_store().setdefault(
            spec_name, _default_inputs_type_spec(self, spec_name)
        )
    return type_spec_store().get(spec_name)


def outputs_type_spec(self):
    spec_name = f"{u0(self.name)}Output"
    if not type_spec_store().has(spec_name):
        type_spec_store().setdefault(
            spec_name, _default_outputs_type_spec(self, spec_name)
        )
    return type_spec_store().get(spec_name)
