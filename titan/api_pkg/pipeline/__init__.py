import moonleap.resource.props as P
from moonleap import MemFun, Prop, create, empty_rule, extend, named
from moonleap.verbs import connects
from titan.api_pkg.itemlist.resources import ItemList

from . import props
from .resources import Pipeline

rules = [
    (("x+pipeline", connects, "+pipeline-elm"), empty_rule()),
    (("x+pipeline", connects, "api-endpoint"), empty_rule()),
    (("x+pipeline", connects, "state"), empty_rule()),
]


@create("pipeline")
def create_pipeline(term):
    pipeline = Pipeline()
    return pipeline


@create("x+pipeline")
def create_named_pipeline(term):
    return named(Pipeline)()


@extend(named(Pipeline))
class ExtendNamedPipeline:
    bvrs = Prop(props.bvrs)
    get_bvr = MemFun(props.get_bvr)
    deleter_mutation = Prop(props.deleter_mutation)
    elements = Prop(props.elements)
    input_expression = Prop(props.input_expression)
    output = Prop(props.output)
    resources = P.children(connects, "+pipeline-elm")
    root_pipeline = Prop(props.root_pipeline)
    root_query = P.child(connects, "api-endpoint")
    root_state = P.child(connects, "state")
    status_expression = Prop(props.status_expression)


@extend(named(ItemList))
class ExtendNamedItemList:
    pipeline = P.parent("x+pipeline", connects)
