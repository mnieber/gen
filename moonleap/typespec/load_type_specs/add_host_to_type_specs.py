def add_host_to_type_specs(host, type_spec_store):
    for type_spec in type_spec_store.type_specs():
        for field_spec in type_spec.get_field_specs():
            # By default, if the fk field is in the server api,
            # then it exists in the client
            if "server" in field_spec.has_api:
                field_spec.has_model.append(host)
                field_spec.has_api.append(host)

            # By default, if the field is optional in the server host,
            # then it's optional in the new host as well.
            if "server" in field_spec.optional:
                field_spec.optional.append(host)
