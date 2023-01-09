from jdoc.packages import *
from jdoc.scenario import *


@dataclass
class Relation(Entity):
    subj: str = field(init=False)
    subj_res: Entity = field(init=False)
    obj: str = field(init=False)
    obj_res: Entity = field(init=False)
    verb: str = field(init=False)


def create_relation(subj: str, verb: str, obj: str) -> Relation:
    rel = Relation()
    rel.subj = subj
    rel.verb = verb
    rel.obj = obj
    return rel


@dataclass
class Action(Entity):
    rule: Rule
    src_rel: Relation


@dataclass
class Forwards(Entity):
    relations: list[Relation] = field(default_factory=list)


@dataclass
class Actions(Entity):
    actions: list[Action] = field(default_factory=list)
