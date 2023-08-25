def get_helpers(_):
    class Helpers:
        type_spec = _.type_spec
        django_module = type_spec.django_module
        model_field_specs = [x for x in type_spec.get_field_specs() if x.has_model]
        field_specs = sorted(
            [x for x in type_spec.get_field_specs() if is_api_field(x)],
            key=lambda x: x.name,
        )
        type_specs = sorted(
            [
                x.target_type_spec
                for x in type_spec.get_field_specs(["fk", "relatedSet"])
                if is_api_field(x) and x.target_type_spec
            ],
            key=lambda x: x.type_name,
        )
        __import__("pudb").set_trace()  # zz

        @property
        def excluded_field_specs(self):
            derived_field_names = [x.name for x in self.field_specs]
            result = [
                field_spec
                for field_spec in self.model_field_specs
                if not field_spec.has_api and field_spec.name not in derived_field_names
            ]
            return sorted(result, key=lambda x: x.name)

    return Helpers()


def is_api_field(field_spec):
    return field_spec.field_type == "tags" or (
        field_spec.has_api and not field_spec.has_model
    )
