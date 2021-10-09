from moonleap.typespec.type_spec import form_type_spec_from_data_type_spec
from moonleap.typespec.type_spec_store import type_spec_store
from titan.api_pkg.pkg.ml_name import (
    ml_form_type_name_from_type_name,
    ml_type_name_from_item_name,
)


def get_or_create_form_type_spec(item_name):
    data_type_name = ml_type_name_from_item_name(item_name)
    form_type_name = ml_form_type_name_from_type_name(data_type_name)
    form_type_spec = type_spec_store().get(form_type_name, None)
    if form_type_spec:
        return form_type_spec

    data_type_spec = type_spec_store().get(data_type_name)
    form_type_spec = form_type_spec_from_data_type_spec(data_type_spec)
    type_spec_store().setdefault(form_type_name, form_type_spec)
    return form_type_spec
