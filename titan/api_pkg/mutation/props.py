from moonleap import u0
from moonleap.resources.field_spec import FieldSpec
from moonleap.resources.type_spec_store import TypeSpec, type_spec_store
from titan.api_pkg.mutation.default_outputs_type_spec import default_outputs_type_spec


def _field_spec_from_item(self, item):
    return FieldSpec(
        name_snake=item.item_name_snake + "_form",
        name=item.item_name + "Form",
        required=False,
        private=False,
        field_type="form",
        field_type_attrs=dict(target=item.item_name),
    )


def _default_inputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            *[_field_spec_from_item(self, item) for item in self.items_posted],
        ],
    )


def inputs_type_spec(self):
    type_spec_name = f"{u0(self.name)}Inputs"
    type_spec = type_spec_store().get(type_spec_name, None)
    if not type_spec:
        type_spec = _default_inputs_type_spec(self, type_spec_name)
        type_spec_store().setdefault(type_spec_name, type_spec)

    return type_spec_store().get(type_spec_name)


def outputs_type_spec(self):
    name = f"{u0(self.name)}Outputs"
    if not type_spec_store().has(name):
        type_spec_store().setdefault(name, default_outputs_type_spec(self, name))
    return type_spec_store().get(name)


def posts_item(self, item_name):
    return [x for x in self.items_posted if x.item_name == item_name]
