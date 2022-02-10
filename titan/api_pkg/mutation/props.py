from moonleap import u0
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec, type_spec_store
from titan.api_pkg.mutation.default_outputs_type_spec import default_outputs_type_spec


def _field_spec_from_item(self, item):
    return FieldSpec(
        name=item.item_name + "Form",
        required=False,
        private=False,
        field_type="form",
        field_type_attrs=dict(target=item.item_type.name),
    )


def _field_spec_from_deleted_item_list(self, item_list):
    return FieldSpec(
        name=item_list.item_name + "Ids",
        required=True,
        private=False,
        field_type="idList",
        field_type_attrs=dict(target=item_list.item_type.name),
    )


def _default_inputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            *[_field_spec_from_item(self, item) for item in self.items_posted],
            *[
                _field_spec_from_deleted_item_list(self, item_list)
                for item_list in self.item_lists_deleted
            ],
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
