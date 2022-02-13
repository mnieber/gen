from moonleap.utils.fp import add_to_list_as_set
from titan.api_pkg.pipeline.props import TakeItemFromState, TakeItemListFromState
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)


def create_router_configs(self, named_component):
    result = []

    if self.state:
        router_config = create_component_router_config(
            self,
            named_component=named_component,
            wraps=True,
            url=get_component_base_url(self, ""),
        )
        result.append(router_config)

    return result


def get_context(state_provider):
    _ = lambda: None
    _.state = state_provider.state
    _.has_behaviors = bool(_.state.has_bvrs)

    _.input_items = list()
    _.input_item_lists = list()
    for pipeline in _.state.pipelines:
        input_elm = pipeline.elements[0]
        if isinstance(input_elm, TakeItemFromState):
            add_to_list_as_set(_.input_items, input_elm.obj)
        if isinstance(input_elm, TakeItemListFromState):
            add_to_list_as_set(_.input_item_lists, input_elm.obj)

    _.queries = list()
    for pipeline in _.state.pipelines:
        if pipeline.root_query:
            add_to_list_as_set(_.queries, pipeline.root_pipeline.root_query)

    _.mutations = list()
    for pipeline in _.state.pipelines:
        if pipeline.get_bvr("deletion") and pipeline.target.deleter_mutations:
            add_to_list_as_set(_.mutations, pipeline.target.deleter_mutations[0])

    class Sections:
        pass

    return dict(sections=Sections(), _=_)
