from moonleap.utils.fp import append_uniq
from titan.api_pkg.pipeline.props import (
    ExtractItemListFromItem,
    TakeHighlightedElmFromStateProvider,
    TakeItemFromStateProvider,
    TakeItemListFromStateProvider,
)


def get_helpers(_):
    class Helpers:
        state = _.component.state
        pipelines = _.component.pipelines

        input_items = list()
        pipeline_by_container = list()
        input_item_lists = list()
        queries = list()
        mutations = list()

        def __init__(self):
            self._get_pipeline_sources()
            if self.state:
                self._get_pipeline_by_container()

        def _get_pipeline_sources(self):
            for pipeline in self.pipelines:
                if pipeline.root_query:
                    endpoints = (
                        self.queries
                        if pipeline.root_query.meta.term.tag == "query"
                        else self.mutations
                    )
                    endpoints.append(pipeline.root_query)
                elif pipeline.root_state_provider:
                    pipeline_elm = pipeline.elements[1]
                    if isinstance(
                        pipeline_elm,
                        (
                            TakeItemFromStateProvider,
                            TakeHighlightedElmFromStateProvider,
                            ExtractItemListFromItem,
                        ),
                    ):
                        self.input_items.append(pipeline_elm.subj)
                    elif isinstance(pipeline_elm, TakeItemListFromStateProvider):
                        self.input_item_lists.append(pipeline_elm.subj)

            for container in self.state.containers:
                if delete_items_mutation := container.delete_items_mutation:
                    append_uniq(self.mutations, delete_items_mutation)
                if delete_item_mutation := container.delete_item_mutation:
                    append_uniq(self.mutations, delete_item_mutation)

        def _get_pipeline_by_container(self):
            for container in self.state.containers:
                pipeline = self.get_pipeline(container)
                if pipeline:
                    self.pipeline_by_container.append((container, pipeline))

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

    return Helpers()
