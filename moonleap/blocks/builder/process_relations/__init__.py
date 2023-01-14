import typing as T

from moonleap.blocks.builder.process_relations.find_or_create_resource import (
    find_or_create_resource,
)
from moonleap.blocks.verbs import _is_created_as
from moonleap.packages.rule import Action
from moonleap.resources.relations.rel import Rel


def process_relations(relations: T.List[Rel], actions):
    for rel in relations:
        rel.block.register_relation(rel)

        if not rel.subj_res:
            rel.subj_res = find_or_create_resource(rel.block, rel.origin, rel.subj)

        if not rel.obj_res:
            rel.obj_res = find_or_create_resource(rel.block, rel.origin, rel.obj)

        if not rel.subj_res.has_relation(rel, rel.obj_res):
            rel.subj_res.add_relation(rel, rel.obj_res)

            rules = _find_rules(rel)
            if not rules and rel.verb != _is_created_as:
                raise Exception(f"Unmatched relation ({rel}) in block: {rel.block}")

            for rule in rules:
                _add_action(actions, Action(rule, rel))


def _find_rules(rel):
    rules = []

    for scope in rel.block.get_scopes():
        for rule in scope.find_rules(
            rel,
            subj_base_tags=rel.subj_res.meta.base_tags,
            obj_base_tags=rel.obj_res.meta.base_tags,
        ):
            rules.append(rule)

    return rules


def _add_action(actions, action: Action):
    p = action.rule.priority
    for i in range(len(actions)):
        if actions[i].rule.priority >= p:
            actions.insert(i, action)
            break
    else:
        actions.append(action)
