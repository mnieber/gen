def get_helpers(_):
    class Helpers:
        public_items = _.api_reg.get_public_items(
            lambda field_spec: "server" in field_spec.has_api
        )
        public_items_provided_by_django = [x for x in public_items if x.django_module]
        form_type_specs = _.api_reg.get_form_type_specs()

    return Helpers()
