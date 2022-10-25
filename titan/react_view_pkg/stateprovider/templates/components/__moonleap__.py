from titan.api_pkg.pipeline.props import (
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
            for pipeline in self.pipelines:
                if pipeline.root_query:
                    enpoints = (
                        self.queries
                        if pipeline.root_query.meta.term.tag == "query"
                        else self.mutations
                    )
                    enpoints.append(pipeline.root_query)
                elif pipeline.root_state_provider:
                    pipeline_elm = pipeline.elements[1]
                    if isinstance(
                        pipeline_elm,
                        (
                            TakeItemFromStateProvider,
                            TakeHighlightedElmFromStateProvider,
                        ),
                    ):
                        self.input_items.append(pipeline_elm.obj)
                    elif isinstance(pipeline_elm, TakeItemListFromStateProvider):
                        self.input_item_lists.append(pipeline_elm.obj)

            if self.state:
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
