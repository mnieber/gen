from moonleap import u0
from moonleap.utils.fp import append_uniq
from moonleap.utils.inflect import plural
from titan.types_pkg.typeregistry import get_type_reg


def get_helpers(_):
    class Helpers:
        state_provider = _.component
        state = state_provider.state
        containers = state.containers if state else []
        pipelines = state_provider.pipelines

        queries = list()
        mutations = list()
        type_specs_to_import = list()

        def __init__(self):
            self._get_queries_from_pipelines()
            self._get_mutations_from_containers()
            self._get_types_to_import()

        def _get_queries_from_pipelines(self):
            for pipeline in self.pipelines:
                pipeline_source = pipeline.source
                if pipeline_source.meta.term.tag == "query":
                    append_uniq(self.queries, pipeline_source)
                if pipeline_source.meta.term.tag == "mutation":
                    append_uniq(self.mutations, pipeline_source)

        def _get_mutations_from_containers(self):
            for container in self.containers:
                if delete_items_mutation := container.delete_items_mutation:
                    append_uniq(self.mutations, delete_items_mutation)
                if delete_item_mutation := container.delete_item_mutation:
                    append_uniq(self.mutations, delete_item_mutation)
                if order_items_mutation := container.order_items_mutation:
                    append_uniq(self.mutations, order_items_mutation)

        def container_inputs(
            self, container=None, named_items=True, named_item_lists=True
        ):
            result = []
            for container in [container] if container else self.containers:
                if named_items:
                    for named_item in container.named_items:
                        result.append(named_item)
                if named_item_lists:
                    if container.named_item_list:
                        result.append(container.named_item_list)
            return result

        def _get_types_to_import(self):
            for mutation in self.mutations:
                for field in mutation.api_spec.get_inputs(
                    ["fk", "relatedSet", "uuid", "uuid[]"]
                ):
                    append_uniq(self.type_specs_to_import, field.target_type_spec)

            for named_prop in self.state_provider.named_props:
                res = named_prop.typ
                item = res.item if res.meta.term.tag == "item~list" else res
                append_uniq(self.type_specs_to_import, item.type_spec)

        def delete_items_data(self, container):
            deletes_items = container.get_bvr("deletion")
            data = dict(deletes_items=deletes_items)

            if deletes_items:
                if container.delete_items_mutation:
                    data["deleteMyItems"] = container.delete_items_mutation.name
                    data["myItemIds"] = _get_field_name(
                        container.delete_items_mutation, ["uuid[]"]
                    )
                elif container.delete_item_mutation:
                    data["deleteMyItem"] = container.delete_item_mutation.name
                    data["myItemId"] = _get_field_name(
                        container.delete_item_mutation, ["uuid", "string"]
                    )
            return data

        def order_items_data(self, container):
            mutation = container.order_items_mutation
            orders_items = container.get_bvr("dragAndDrop") and mutation
            data = dict(orders_items=orders_items)
            if orders_items:
                for (
                    parent_type_name,
                    parent_key,
                ) in mutation.api_spec.orders:
                    field_spec = (
                        get_type_reg()
                        .get(u0(parent_type_name))
                        .get_field_spec_by_key(parent_key)
                    )

                    if field_spec.target == container.item.type_spec.type_name:
                        ids_field_name = _get_field_name(mutation, ["uuid[]"])
                        data["otherKeys"] = [
                            x.key
                            for x in mutation.api_spec.get_inputs()
                            if x.key != ids_field_name
                        ]
                        data["orderMyItems"] = mutation.name
                        data["myItems"] = plural(container.item.item_name)
                        data["myItemIds"] = ids_field_name
            return data

        def return_value(self, data, hint=None):
            if data in self.state_provider.named_items_provided:
                pipeline, data_path = self.state_provider.get_pipeline_and_data_path(
                    data
                )
                maybe_expr = self.state_provider.maybe_expression(data)
                return f"maybe({maybe_expr})({data_path})" if maybe_expr else data_path

            if data in self.state_provider.named_item_lists_provided:
                pipeline, data_path = self.state_provider.get_pipeline_and_data_path(
                    data
                )
                maybe_expr = self.state_provider.maybe_expression(data)
                return (
                    f"maybe({maybe_expr})({data_path}, [])" if maybe_expr else data_path
                )

            if data in self.containers and hint == "items":
                container = data
                named_item_list = data.named_item_list
                items_name = plural(container.item.item_name)
                assert named_item_list
                maybe_expr = self.state_provider.maybe_expression(named_item_list)
                data_path = f"state.{container.name}.data.{items_name}Display"
                return (
                    f"maybe({maybe_expr}, [])({data_path})" if maybe_expr else data_path
                )

            if data in self.containers and hint == "highlighted_item":
                container = data
                named_item_list = data.named_item_list
                assert named_item_list
                maybe_expr = self.state_provider.maybe_expression(named_item_list)
                data_path = f"state.{container.name}.highlight.item"
                return f"maybe({maybe_expr})({data_path})" if maybe_expr else data_path

        def get_data_path(self, named_output):
            pipeline, data_path = self.state_provider.get_pipeline_and_data_path(
                named_output
            )
            return data_path

    return Helpers()


def _get_field_name(mutation, field_types):
    for field_type in field_types:
        for field in mutation.api_spec.get_inputs([field_type]):
            return field.name
    raise Exception("Unknown field name")
