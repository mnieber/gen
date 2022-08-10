from titan.api_pkg.typeregistry import get_type_reg
from titan.react_pkg.apimodule.graphql_body import graphql_body


def get_helpers(_):
    class Helpers:
        input_field_specs = _.mutation.inputs_type_spec.field_specs
        form_input_field_specs = [
            x for x in input_field_specs if x.field_type == "form"
        ]
        fk_output_field_specs = _.mutation.outputs_type_spec.get_field_specs(
            ["relatedSet", "fk"]
        )

        def get_graphql_body(self):
            return graphql_body(_.mutation.outputs_type_spec, recurse=False)

        @property
        def invalidated_queries(self):
            result = []
            for item_list in _.mutation.item_lists_deleted:
                for query in _.mutation.graphql_api.queries:
                    for named_item in query.named_items_provided:
                        if named_item.typ.item_name == item_list.item_name:
                            result.append(query)
            return result

        @property
        def form_input_item_types(self):
            result = []
            for field_spec in self.form_input_field_specs:
                item_type = get_type_reg().get_item_type_by_name(field_spec.target)
                result.append(item_type)
            return result

    return Helpers()
