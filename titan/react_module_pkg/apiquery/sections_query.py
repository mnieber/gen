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

    def graphql_body(self, query):
        return graphql_body(query.outputs_type_spec)
