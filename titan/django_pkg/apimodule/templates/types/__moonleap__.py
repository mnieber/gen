def get_helpers(_):
    class Helpers:
        items = [x for x in _.type_reg.items if x.django_module]
        public_items = _.gql_reg.get_public_items("server")

    return Helpers()
