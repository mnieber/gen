from moonleap.utils.fp import append_uniq


# Return all form-type inputs for all queries and mutations
def get_form_type_specs(api_reg):
    result = []

    for mutation in api_reg.get_mutations():
        for field_spec in mutation.api_spec.get_inputs(["form"]):
            append_uniq(result, field_spec.target_type_spec)

    for query in api_reg.get_queries():
        for field_spec in query.api_spec.get_inputs(["form"]):
            append_uniq(result, field_spec.target_type_spec)

    return result
