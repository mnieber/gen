from moonleap.utils.fp import add_to_list_as_set
from titan.api_pkg.pipeline.props import TakeItemFromState, TakeItemListFromState


def get_helpers(_):
    class Helpers:
        state = _.component
        has_behaviors = bool(state.has_bvrs)

        input_items = list()
        input_item_lists = list()
        queries = list()
        mutations = list()

        def __init__(self):
            for pipeline in self.state.pipelines:
                input_elm = pipeline.elements[0]
                if isinstance(input_elm, TakeItemFromState):
                    add_to_list_as_set(self.input_items, input_elm.obj)
                if isinstance(input_elm, TakeItemListFromState):
                    add_to_list_as_set(self.input_item_lists, input_elm.obj)

            for pipeline in self.state.pipelines:
                if pipeline.root_query:
                    add_to_list_as_set(self.queries, pipeline.root_pipeline.root_query)

            for pipeline in self.state.pipelines:
                if pipeline.get_bvr("deletion") and pipeline.target.deleter_mutations:
                    add_to_list_as_set(
                        self.mutations, pipeline.target.deleter_mutations[0]
                    )

    return Helpers()
