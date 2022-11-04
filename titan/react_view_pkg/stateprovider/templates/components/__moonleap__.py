from moonleap.utils.fp import append_uniq
from moonleap.utils.inflect import plural


def get_helpers(_):
    class Helpers:
        state = _.component.state
        pipelines = _.component.pipelines

        input_items = list()
        data_by_container = list()
        input_item_lists = list()
        queries = list()
        mutations = list()
        types_to_import = list()

        def __init__(self):
            self._get_pipeline_sources()
            if self.state:
                self._get_data_by_container()
            self._get_types_to_import()

        def _get_pipeline_sources(self):
            for pipeline in self.pipelines:
                pipeline_source = pipeline.source
                if pipeline_source.meta.term.tag == "query":
                    self.queries.append(pipeline_source)
                elif pipeline_source.meta.term.tag == "mutation":
                    self.mutations.append(pipeline_source)
                elif pipeline_source.meta.term.tag == "item":
                    self.input_items.append(pipeline_source)
                elif pipeline_source.meta.term.tag == "item_list":
                    self.input_item_lists.append(pipeline_source)
                else:
                    raise Exception("Unknown pipeline source")

            for container in self.state.containers:
                if delete_items_mutation := container.delete_items_mutation:
                    append_uniq(self.mutations, delete_items_mutation)
                if delete_item_mutation := container.delete_item_mutation:
                    append_uniq(self.mutations, delete_item_mutation)
                if order_items_mutation := container.order_items_mutation:
                    append_uniq(self.mutations, order_items_mutation)

        def _get_data_by_container(self):
            for container in self.state.containers:
                pipeline = self.get_pipeline(container)
                if pipeline:
                    self.data_by_container.append((container, dict(pipeline=pipeline)))

        def _get_types_to_import(self):
            for mutation in self.mutations:
                for field in mutation.gql_spec.get_inputs(
                    ["fk", "relatedSet", "uuid", "uuid[]"]
                ):
                    append_uniq(self.types_to_import, field.target + "T")

        def get_pipeline(self, named_output_or_container):
            if named_output_or_container.meta.term.tag == "container":
                container = named_output_or_container
                named_item = container.named_item_list or container.named_item
                if named_item:
                    return self.get_pipeline(named_item)
            else:
                for pipeline in self.pipelines:
                    if named_output_or_container == pipeline.output:
                        return pipeline
            return None

        def maybe_expr(self, named_item_or_item_list):
            pipeline = self.get_pipeline(named_item_or_item_list)
            pipeline_source = pipeline.source
            if pipeline_source.meta.term.tag in ("query", "mutation"):
                return pipeline_source.name
            elif pipeline_source.meta.term.tag in ("item",):
                return f"props.{pipeline_source.item_name}"
            else:
                return f"props.{plural(pipeline_source.item.item_name)}"

        def delete_items_expr(self, container):
            if container.delete_items_mutation:
                name = container.delete_items_mutation.name
                field_name = _get_field_name(
                    container.delete_items_mutation, ["uuid[]"]
                )
                return f"return {name}.mutateAsync({{{field_name}: ids}});"
            elif container.delete_item_mutation:
                name = container.delete_item_mutation.name
                field_name = _get_field_name(
                    container.delete_item_mutation, ["uuid", "string"]
                )
                return (
                    "return Promise.all(R.map((x: string) => "
                    + f"{name}.mutateAsync({{{field_name}: x}}), ids));"
                )

        def order_items_expr(self, container):
            if container.order_items_mutation:
                name = container.order_items_mutation.name
                items = plural(container.item_name)
                field_name = _get_field_name(
                    container.delete_items_mutation, ["uuid[]"]
                )
                return f"return {name}.mutateAsync({{{field_name}: getIds({items})}});"

    return Helpers()


def _get_field_name(mutation, field_types):
    for field_type in field_types:
        for field in mutation.gql_spec.get_inputs([field_type]):
            return field.name
    raise Exception("Unknown field name")
