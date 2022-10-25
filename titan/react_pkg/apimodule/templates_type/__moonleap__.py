from titan.react_pkg.apimodule.graphql_body import (
    get_dependency_type_specs,
    graphql_body,
)


def get_helpers(_):
    class Helpers:
        field_specs = sorted(
            [x for x in _.item.type_spec.get_field_specs() if "client" in x.has_model],
            key=lambda x: x.key,
        )
        fk_field_specs = [
            x for x in field_specs if x.field_type in ("fk", "relatedSet")
        ]
        form_field_specs = [
            x
            for x in _.item.form_type_spec.get_field_specs()
            if "client" in x.has_model
        ]

        def graphql_fields(self):
            type_specs_to_import, body = graphql_body(
                _.item.type_spec, define_type=True, indent=2
            )
            return body

        @property
        def dependency_type_specs(self):
            return get_dependency_type_specs(_.item.type_spec, recurse=True)

    return Helpers()
