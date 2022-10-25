def get_helpers(_):
    class Helpers:
        items = [x for x in _.type_reg.items if x.django_module]
        public_items = _.gql_reg.get_public_items(
            lambda field_spec: "server" in field_spec.has_api
        )
        form_type_specs = _.gql_reg.get_form_type_specs()

    return Helpers()
