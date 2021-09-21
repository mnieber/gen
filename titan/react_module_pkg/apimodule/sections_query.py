import os

from moonleap.utils.case import lower0
from moonleap.utils.fp import ds
from titan.react_module_pkg.apimodule.utils import (
    field_spec_to_graphql_arg,
    graphql_body,
    javascript_args,
)


class SectionsQuery:
    def __init__(self, res):
        self.res = res

    def javascript_args(self, query):
        return javascript_args(query.inputs_type_spec)

    def graphql_args(self, query, before):
        tab = " " * (4 if before else 8)
        field_specs = query.inputs_type_spec.field_specs
        if not field_specs:
            return ""

        return (
            "("
            + os.linesep
            + os.linesep.join(
                map(
                    lambda t: tab + "  " + field_spec_to_graphql_arg(t.name, t, before),
                    field_specs,
                )
            )
            + os.linesep
            + tab
            + ")"
        )

    def graphql_body(self, query):
        return graphql_body(query.outputs_type_spec)

    def graphql_variables(self, query):
        tab = " " * 6
        field_specs = query.inputs_type_spec.field_specs
        return tab + ("," + os.linesep + tab).join(
            [field_spec.name for field_spec in field_specs]
        )

    def graphql_response(self, query):
        schema = lower0(query.outputs_type_spec.type_name)
        return f"return normalize(response, {schema}).entities"
