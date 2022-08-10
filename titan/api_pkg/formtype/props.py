from moonleap.typespec.type_spec import form_type_spec_from_data_type_spec
from moonleap.typespec.type_spec_store import type_spec_store


def get_or_create_form_type_spec(form_type):
    form_type_spec = type_spec_store().get(form_type.name)
    if form_type_spec:
        return form_type_spec

    data_type_spec = type_spec_store().get(form_type.type_name)
    form_type_spec = form_type_spec_from_data_type_spec(data_type_spec, form_type.name)
    type_spec_store().setdefault(form_type.type_name, form_type_spec)
    return form_type_spec


def form_type_type_spec(form_type):
    return type_spec_store().get(form_type.name)
