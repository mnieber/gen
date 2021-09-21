from dataclasses import replace

import ramda as R
from moonleap import upper0
from moonleap.resources.type_spec_store import FieldSpec, TypeSpec, type_spec_store


def _form_type_spec_from_data_type_spec(data_type_spec):
    def _convert(field_spec):
        changes = {}
        if field_spec.field_type in ("fk",):
            changes = dict(
                field_type="uuid",
                field_type_attrs={},
            )

        return replace(field_spec, **changes)

    return TypeSpec(
        type_name=data_type_spec.type_name + "Form",
        field_specs=R.pipe(
            R.always(data_type_spec.field_specs),
            R.filter(lambda x: x.field_type != "related_set"),
            R.map(_convert),
        )(None),
    )


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


def _create_form_type_spec(type_name):
    data_type_name = upper0(type_name)  # HACK
    data_type_spec = type_spec_store().get(data_type_name)

    form_type_name = upper0(type_name + "Form")  # HACK
    form_type_spec = type_spec_store().get(form_type_name, None)

    if form_type_spec is None:
        type_spec_store().setdefault(
            form_type_name, _form_type_spec_from_data_type_spec(data_type_spec)
        )


def inputs_type_spec(self):
    name = f"{upper0(self.name)}Input"
    if not type_spec_store().has(name):
        inputs_type_spec = _default_inputs_type_spec(self, name)
        for field_spec in inputs_type_spec.field_specs:
            if field_spec.field_type in ("fk",):
                fk_type_name = field_spec.field_type_attrs["target"]
                _create_form_type_spec(fk_type_name)

        type_spec_store().setdefault(name, inputs_type_spec)
    return type_spec_store().get(name)


def outputs_type_spec(self):
    name = f"{upper0(self.name)}Output"
    if not type_spec_store().has(name):
        type_spec_store().setdefault(name, _default_outputs_type_spec(self, name))
    return type_spec_store().get(name)
