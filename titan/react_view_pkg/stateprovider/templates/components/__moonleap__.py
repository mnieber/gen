from moonleap import u0
from moonleap.utils.fp import append_uniq
from moonleap.utils.inflect import plural
from titan.api_pkg.pipeline.resources import PipelineData
from titan.types_pkg.typeregistry import get_type_reg


def get_helpers(_):
    class Helpers:
        state_provider = _.component
        state = state_provider.state
        containers = state.containers if state else []
        pipelines = state_provider.pipelines

        data = PipelineData()
        type_specs_to_import = list()

        def __init__(self):
            self.data.update(self.pipelines)
            self._get_mutations_from_containers()
            self._get_types_to_import()

        def _get_mutations_from_containers(self):
            for container in self.containers:
                if delete_items_mutation := container.delete_items_mutation:
                    append_uniq(self.data.mutations, delete_items_mutation)
                if delete_item_mutation := container.delete_item_mutation:
                    append_uniq(self.data.mutations, delete_item_mutation)
                if order_items_mutation := container.order_items_mutation:
                    append_uniq(self.data.mutations, order_items_mutation)

        def _get_types_to_import(self):
            for mutation in self.data.mutations:
                for field in mutation.api_spec.get_inputs(
                    ["fk", "relatedSet", "uuid", "uuid[]"]
                ):
                    append_uniq(self.type_specs_to_import, field.target_type_spec)

            for prop_item in self.data.prop_items:
                append_uniq(self.type_specs_to_import, prop_item.type_spec)

            for prop_item_list in self.data.prop_item_lists:
                append_uniq(self.type_specs_to_import, prop_item_list.item.type_spec)

        def get_pipeline(self, named_output_or_container):
            if named_output_or_container.meta.term.tag == "container":
                container = named_output_or_container
                named_item = container.named_item_list or container.named_item
                if named_item:
                    return self.get_pipeline(named_item)
            else:
                for pipeline in self.pipelines:
                    if named_output_or_container.typ == pipeline.output.typ:
                        return pipeline
            return None

        def maybe_expr(self, named_item_or_item_list):
            pipeline = self.get_pipeline(named_item_or_item_list)
            if not pipeline:
                return "'Moonleap Todo'"

            pipeline_source = pipeline.source
            if pipeline_source.meta.term.tag in ("query", "mutation"):
                return pipeline_source.name
            elif pipeline_source.meta.term.tag in ("item",):
                return f"props.{pipeline_source.item_name}"
            elif pipeline_source.meta.term.tag in ("props",):
                return None
            else:
                return f"props.{plural(pipeline_source.item.item_name)}"

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
            result_expr = self.get_pipeline(data).result_expression()
            if data in self.state_provider.named_items_provided:
                maybe_expr = self.maybe_expr(data)
                return (
                    f"maybe({maybe_expr})({result_expr})" if maybe_expr else result_expr
                )

            if data in self.state_provider.named_item_lists:
                maybe_expr = self.maybe_expr(data)
                return (
                    f"maybe({maybe_expr})({result_expr}, [])"
                    if maybe_expr
                    else result_expr
                )

            if data in self.containers and hint == "items":
                container = data
                named_item_list = data.named_item_list
                items_name = plural(container.item.item_name)
                assert named_item_list
                maybe_expr = self.maybe_expr(named_item_list)
                result_expr = f"state.{container.name}.data.{items_name}Display"
                return (
                    f"maybe({maybe_expr}, [])({result_expr})"
                    if maybe_expr
                    else result_expr
                )

            if data in self.containers and hint == "highlighted_item":
                container = data
                named_item_list = data.named_item_list
                assert named_item_list
                maybe_expr = self.maybe_expr(named_item_list)
                result_expr = f"state.{container.name}.highlight.item"
                return (
                    f"maybe({maybe_expr})({result_expr})" if maybe_expr else result_expr
                )

    return Helpers()


def _get_field_name(mutation, field_types):
    for field_type in field_types:
        for field in mutation.api_spec.get_inputs([field_type]):
            return field.name
    raise Exception("Unknown field name")
