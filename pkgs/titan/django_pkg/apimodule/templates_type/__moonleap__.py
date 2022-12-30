def get_helpers(_):
    class Helpers:
        type_spec = _.type_spec
        django_module = type_spec.django_module
        model_field_specs = [
            x for x in type_spec.get_field_specs() if "server" in x.has_model
        ]
        derived_field_specs = [
            x
            for x in type_spec.get_field_specs()
            if ("server" in x.has_api and "server" not in x.has_model)
        ]

        @property
        def excluded_field_specs(self):
            derived_field_names = [x.name for x in self.derived_field_specs]
            result = [
                field_spec
                for field_spec in self.model_field_specs
                if "server" not in field_spec.has_api
                and field_spec.name not in derived_field_names
            ]
            return result

    return Helpers()
