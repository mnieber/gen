from titan.types_pkg.typeregistry import get_type_reg


def django_model_form_field_spec(django_model):
    form_spec_type_name = django_model.type_spec.type_name + "Form"
    return get_type_reg().get(form_spec_type_name, None)
