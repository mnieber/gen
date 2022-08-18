from titan.react_pkg.apimodule.graphql_body import (
    get_dependency_type_specs,
    graphql_body,
)


def get_helpers(_):
    class Helpers:
        field_specs = [
            x for x in _.item.type_spec.get_field_specs() if "client" in x.api
        ]
        fk_field_specs = [
            x
            for x in _.item.type_spec.get_field_specs(["fk", "relatedSet"])
            if "client" in x.api
        ]
        form_field_specs = [x for x in _.item.form_type_spec.get_field_specs()]

        def graphql_fields(self):
            return graphql_body(_.item.type_spec, recurse=True)

        @property
        def dependency_type_specs(self):
            return get_dependency_type_specs(_.item.type_spec, recurse=True)

    return Helpers()
