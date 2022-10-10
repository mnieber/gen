import ramda as R


def comp(lhs_model, rhs_model):
    for field_spec in lhs_model.type_spec.get_field_specs(["fk", "relatedSet"]):
        if field_spec.target == rhs_model.name:
            return +1
    for field_spec in rhs_model.type_spec.get_field_specs(["fk", "relatedSet"]):
        if field_spec.target == lhs_model.name:
            return -1
    return 0


def sort_django_models(django_models):
    return R.sort(comp, django_models)
