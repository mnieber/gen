import moonleap.resource.props as P
from moonleap import tags
from moonleap.verbs import has

from .resources import Behavior


@tags(["behavior"])
def create_behavior(term, block):
    behavior = Behavior()
    return behavior
