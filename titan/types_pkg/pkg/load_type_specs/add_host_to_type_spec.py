from moonleap.utils.fp import append_uniq


def add_host_to_type_spec(host, type_spec):
    for field_spec in type_spec.get_field_specs():
        # By default, if the field is in the server api,
        # then it exists in the client
        if "server" in field_spec.has_api:
            append_uniq(field_spec.has_model, host)
            append_uniq(field_spec.has_api, host)

        # By default, if the field is optional in the server host,
        # then it's optional in the new host as well.
        if field_spec.is_optional("server"):
            append_uniq(field_spec.optional, host)
