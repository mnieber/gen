from titan.types_pkg.pkg.form_type_spec_from_data_type_spec import (
    form_type_spec_from_data_type_spec,
)


def post_process_gql_specs(gql_reg, type_reg):
    for gql_spec in gql_reg.gql_specs():
        for form_field_spec in gql_spec.inputs_type_spec.get_field_specs(["form"]):
            type_name = form_field_spec.target
            form_type_name = type_name + "Form"
            data_type_spec = type_reg.get(type_name)

            form_type_spec = form_type_spec_from_data_type_spec(
                data_type_spec, form_type_name
            )
            type_reg.setdefault(form_type_name, form_type_spec)
