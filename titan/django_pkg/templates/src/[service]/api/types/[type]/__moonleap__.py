from titan.api_pkg.apiregistry.get_public_type_specs import get_public_type_specs


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
                if x.target_type_spec
                and x.target != _.type_spec.type_name
                and x.has_api
            ],
            key=lambda x: x.type_name,
        )

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


def get_meta_data_by_fn(_, __):
    return {
        ".": {"name": ".."},
        "graphql_type.py.j2": {
            "name": f"{_.type_spec.type_name.lower()}_t.py",
        },
    }


def get_contexts(_):
    return [
        dict(type_spec=type_spec)
        for type_spec in get_public_type_specs(
            _.api_reg,
            include_stubs=False,
            predicate=lambda type_spec: not type_spec.no_api,
        )
    ]
