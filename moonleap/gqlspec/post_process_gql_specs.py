from moonleap.typespec.form_type_spec_from_data_type_spec import (
    form_type_spec_from_data_type_spec,
)


def post_process_gql_specs(gql_spec_store, type_spec_store):
    for gql_spec in gql_spec_store.gql_specs():
        for form_field_spec in gql_spec.inputs_type_spec.get_field_specs(["form"]):
            type_name = form_field_spec.target
            form_type_name = type_name + "Form"
            data_type_spec = type_spec_store.get(type_name)

            form_type_spec = form_type_spec_from_data_type_spec(
                data_type_spec, form_type_name
            )
            type_spec_store.setdefault(form_type_name, form_type_spec)
