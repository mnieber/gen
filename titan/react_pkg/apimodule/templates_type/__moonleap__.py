from titan.react_pkg.apimodule.graphql_body import (
    get_dependency_type_specs,
    graphql_body,
)
from titan.types_pkg.pkg.has_hydrated_fields import (
    has_hydrated_fields,
    is_hydrated_field,
)


def get_helpers(_):
    class Helpers:
        hydrated_field_specs = []

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

        def __init__(self):
            self.get_hydrated_fields()

        def graphql_fields(self):
            type_specs_to_import, body = graphql_body(
                _.item.type_spec, define_type=True, indent=2
            )
            return body

        def get_hydrated_fields(self):
            for field_spec in self.field_specs:
                if field_spec.field_type in ("fk", "relatedSet"):
                    if has_hydrated_fields(field_spec.target_type_spec, "client"):
                        self.hydrated_field_specs.append(field_spec)
                elif is_hydrated_field(field_spec, "client"):
                    self.hydrated_field_specs.append(field_spec)

        @property
        def dependency_type_specs(self):
            return get_dependency_type_specs(_.item.type_spec, recurse=True)

    return Helpers()
