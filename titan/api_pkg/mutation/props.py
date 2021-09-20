import ramda as R
from moonleap import upper0
from moonleap.resources.type_spec_store import FieldSpec, TypeSpec, type_spec_store


def _default_inputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            *[_item_field(self, item) for item in self.items_posted],
        ],
    )


def _default_outputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            FieldSpec(
                name_snake="success",
                name="success",
                required=False,
                private=False,
                field_type="boolean",
            ),
            FieldSpec(
                name_snake="errors",
                name="errors",
                required=False,
                private=False,
                field_type="any",
            ),
        ],
    )


def _item_field(self, item):
    return FieldSpec(
        name_snake=item.item_name_snake + "_form",
        name=item.item_name + "Form",
        required=False,
        private=False,
        field_type="fk",
        field_type_attrs=dict(
            target=upper0(item.item_name + "Form"), has_related_set=False
        ),
    )


def inputs_type_spec(self):
    name = f"{upper0(self.name)}Input"
    if not type_spec_store().has(name):
        type_spec_store().setdefault(name, _default_inputs_type_spec(self, name))
    return type_spec_store().get(name)


def outputs_type_spec(self):
    name = f"{upper0(self.name)}Output"
    if not type_spec_store().has(name):
        type_spec_store().setdefault(name, _default_outputs_type_spec(self, name))
    return type_spec_store().get(name)
