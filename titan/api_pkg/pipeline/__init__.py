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
    component = P.parent("component", has)
    data_path = MemFun(props.pipeline_data_path)
    resources = P.children(connects, "x+pipeline-elm")
    source = Prop(props.pipeline_source)
    maybe_expression = MemFun(props.pipeline_maybe_expression)


@extend(named(Pipeline))
class ExtendPrivateNamedPipeline:
    _root_props = P.child(connects, "props")
    _root_query = P.child(connects, "api-endpoint")
    _root_state_provider = P.child(connects, "state~provider")
