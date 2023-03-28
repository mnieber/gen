import typing as T

from jdoc.moonleap.imports import *


class Rule(Entity):
    name: str
    pattern: str

    def run(self, rel: "Relation", forwards: "Forwards"):
        pass


class Relation(Entity):
    subj: str = ""
    subj_res: Entity = None
    verb: str = ""
    obj: str = ""
    obj_res: Entity = None


def create_relation(subj: str, verb: str, obj: str) -> Relation:
    return Relation(subj=subj, verb=verb, obj=obj)


class Action(Entity):
    rule: Rule
    src_rel: Relation


class Forwards(Entity):
    relations: T.List[Relation] = []


class Actions(Entity):
    actions: T.List[Action] = []
