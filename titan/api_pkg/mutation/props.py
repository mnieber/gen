from moonleap import upper0
from moonleap.resources.field_spec import FieldSpec
from moonleap.resources.type_spec import form_type_spec_from_data_type_spec
from moonleap.resources.type_spec_store import TypeSpec, type_spec_store
from titan.api_pkg.mutation.default_outputs_type_spec import default_outputs_type_spec


def _field_spec_from_item(self, item):
    return FieldSpec(
        name_snake=item.item_name_snake + "_form",
        name=item.item_name + "Form",
        required=False,
        private=False,
        field_type="form",
        field_type_attrs=dict(
            target=upper0(item.item_name + "Form"),
            has_related_set=False,
            item_name=item.item_name,
        ),
    )


def _default_inputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            *[_field_spec_from_item(self, item) for item in self.items_posted],
        ],
    )


def _get_or_create_form_type_spec(field_spec):
    form_type_name = field_spec.field_type_attrs["target"]
    form_type_spec = type_spec_store().get(form_type_name, None)
    if form_type_spec:
        return form_type_spec

    data_type_name = upper0(field_spec.field_type_attrs["item_name"])
    data_type_spec = type_spec_store().get(data_type_name)
    form_type_spec = form_type_spec_from_data_type_spec(data_type_spec)
    type_spec_store().setdefault(form_type_spec.type_name, form_type_spec)
    return form_type_spec


def inputs_type_spec(self):
    name = f"{upper0(self.name)}Input"
    inputs_type_spec = type_spec_store().get(name, None)
    if not inputs_type_spec:
        inputs_type_spec = _default_inputs_type_spec(self, name)
        type_spec_store().setdefault(name, inputs_type_spec)

    # Automatically create missing form type specs
    for field_spec in inputs_type_spec.field_specs:
        if field_spec.field_type in ("form",):
            _get_or_create_form_type_spec(field_spec)

    return type_spec_store().get(name)


def outputs_type_spec(self):
    name = f"{upper0(self.name)}Output"
    if not type_spec_store().has(name):
        type_spec_store().setdefault(name, default_outputs_type_spec(self, name))
    return type_spec_store().get(name)


def posts_item(self, item_name):
    return [x for x in self.items_posted if x.item_name == item_name]
