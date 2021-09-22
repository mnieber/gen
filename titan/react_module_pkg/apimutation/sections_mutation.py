import os

from moonleap import upper0
from moonleap.utils.case import lower0
from titan.react_module_pkg.apimodule.utils import (
    field_spec_to_graphql_arg,
    graphql_body,
    javascript_args,
)
from titan.react_pkg.reactapp.resources import find_module_that_provides_item_list


class SectionsMutation:
    def __init__(self, res):
        self.res = res

    def javascript_args(self, mutation):
        return javascript_args(mutation.inputs_type_spec)

    def mutation_imports(self, mutation):
        result = []
        for field_spec in mutation.inputs_type_spec.field_specs:
            if field_spec.field_type == "form":
                item_name = field_spec.field_type_attrs["item_name"]
                ts_module = find_module_that_provides_item_list(
                    self.res.react_app, item_name
                )
                if ts_module:
                    result.append(
                        f"import {{ {upper0(item_name)}T }} from 'src/{ts_module.name}/types"
                    )
        return os.linesep.join(result)

    def graphql_args(self, mutation, before):
        tab = " " * (4 if before else 8)
        field_specs = mutation.inputs_type_spec.field_specs
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

    def graphql_body(self, mutation):
        return graphql_body(mutation.outputs_type_spec)

    def graphql_variables(self, mutation):
        tab = " " * 6
        field_specs = mutation.inputs_type_spec.field_specs
        return tab + ("," + os.linesep + tab).join(
            [field_spec.name for field_spec in field_specs]
        )

    def graphql_response(self, mutation):
        schema = lower0(mutation.outputs_type_spec.type_name)
        return f"return normalize(response, {schema}).entities"
