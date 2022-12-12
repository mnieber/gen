from moonleap.utils.fp import append_uniq


def get_form_type_specs(api_reg):
    result = []

    for mutation in api_reg.mutations:
        for field_spec in mutation.api_spec.get_inputs(["form"]):
            append_uniq(result, field_spec.target_type_spec)

    for query in api_reg.queries:
        for field_spec in query.api_spec.get_inputs(["form"]):
            append_uniq(result, field_spec.target_type_spec)

    return result
