import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, named
from moonleap.verbs import connects

from .resources import Pipeline

rules = [(("+pipeline", connects, "x:x"), empty_rule())]


@create("pipeline")
def create_pipeline(term, block):
    pipeline = Pipeline()
    return pipeline


@create("+pipeline")
def create_named_pipeline(term, block):
    return named(Pipeline)()


@extend(Pipeline)
class ExtendPipeline:
    elements = P.child(connects, "x:x")
