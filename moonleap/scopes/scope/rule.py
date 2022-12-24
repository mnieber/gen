import typing as T
from dataclasses import dataclass
from enum import Enum

from moonleap.blocks.term import word_to_term
from moonleap.resource import Resource
from moonleap.resource.rel import Rel
from moonleap.verbs import is_created_as


class Priorities(Enum):
    HIGH = 100
    NORMAL = 50
    LOW = 10


@dataclass
class Rule:
    rel: Rel
    f: T.Callable
    priority: int = 1

    def __repr__(self):
        verb = (
            f"{self.rel.verb[0]}*"
            if isinstance(self.rel.verb, tuple)
            else self.rel.verb
        )
        return (
            f"Rule({self.rel.subj} /{verb} {self.rel.obj}) "
            + f"triggers {self.f.__name__}"
        )


@dataclass
class Action:
    rule: Rule
    src_rel: Rel
    subj_res: Resource
    obj_res: Resource

    def trace(self):
        result = []
        result.append(self.rule)
        src_rel = self.src_rel
        while src_rel:
            result.append(f"{src_rel} in {src_rel.block}")
            action = src_rel.origin
            if action:
                result.append(action.rule)
                src_rel = action.src_rel
            else:
                result.append(f"{src_rel} in {src_rel.block}")
                src_rel = None

        for x in reversed(result):
            print(x)


def rule(subj_term, verb=None, obj_term=None, priority=Priorities.NORMAL.value):
    if verb is None or obj_term is None:
        if verb is not None or obj_term is not None:
            raise Exception("Either define both verb and obj_term or neither")
        verb = is_created_as
        obj_term = subj_term

    def wrapped(f):
        rel = Rel(
            subj=word_to_term(subj_term, default_to_tag=True),
            verb=verb,
            obj=word_to_term(obj_term, default_to_tag=True),
        )
        f.moonleap_rule = Rule(rel, f, priority=priority)
        return f

    return wrapped
