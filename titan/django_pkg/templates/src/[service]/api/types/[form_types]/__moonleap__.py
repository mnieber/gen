from titan.api_pkg.apiregistry.get_form_type_specs import get_form_type_specs


def get_helpers(_):
    class Helpers:
        field_specs = sorted(
            [x for x in _.form_type_spec.get_field_specs() if x.has_api],
            key=lambda x: x.name,
        )

        def args(self, field_spec):
            return "" if field_spec.is_optional else "required=True"

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        ".": {"name": ".."},
        "graphql_form_type.py.j2": {
            "name": f"{_.form_type_spec.type_name.lower()}_t.py",
        },
    }


def get_contexts(_):
    return [
        dict(form_type_spec=form_type_spec)
        for form_type_spec in get_form_type_specs(_.api_reg)
    ]
