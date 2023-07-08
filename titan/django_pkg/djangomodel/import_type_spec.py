def import_type_spec(type_spec, django_model):
    django_model.type_spec = type_spec
    django_model.name = type_spec.type_name
