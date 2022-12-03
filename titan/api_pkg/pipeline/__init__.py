import moonleap.resource.props as P
from moonleap import MemFun, Prop, create, empty_rule, extend, named
from moonleap.verbs import connects, has

from . import props
from .resources import Pipeline, PropsSource

rules = {
    ("x+pipeline", connects, "x+pipeline-elm"): empty_rule(),
    ("x+pipeline", connects, "api-endpoint"): empty_rule(),
    ("x+pipeline", connects, "state~provider"): empty_rule(),
    ("x+pipeline", connects, "props"): empty_rule(),
}


@create("pipeline")
def create_pipeline(term):
    pipeline = Pipeline()
    return pipeline


@create("props")
def create_props_source(term):
    return PropsSource()


@create("x+pipeline")
def create_named_pipeline(term):
    return named(Pipeline)()


@extend(named(Pipeline))
class ExtendNamedPipeline:
    deleter_mutation = Prop(props.deleter_mutation)
    elements = Prop(props.elements)
    result_data_path = MemFun(props.result_data_path)
    output = Prop(props.output)
    output_name = Prop(props.output_name)
    resources = P.children(connects, "x+pipeline-elm")
    root_pipeline = Prop(props.root_pipeline)
    root_query = P.child(connects, "api-endpoint")
    root_state_provider = P.child(connects, "state~provider")
    root_props = P.child(connects, "props")
    status_expression = Prop(props.status_expression)
    state_provider = P.parent("state~provider", has)
    source = Prop(props.pipeline_source)
