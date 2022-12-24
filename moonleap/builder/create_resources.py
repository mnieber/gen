import typing as T

from moonleap.builder.add_meta_data_to_blocks import add_meta_data_to_blocks
from moonleap.builder.find_relations import get_relations
from moonleap.builder.process_relations import process_relations
from moonleap.resource.rel import Rel
from moonleap.verbs import is_created_as


def _to_list_of_relations(x, action):
    result = list(x) if (isinstance(x, list) or isinstance(x, tuple)) else [x]
    for rel in result:
        if not isinstance(rel, Rel):
            raise Exception(
                f"A rule ({action.rule}) should either return a Rel or a list of Rel"
            )
    return [
        Rel(x.subj, x.verb, x.obj, x.block or action.src_rel.block, origin=action)
        for x in result
    ]


def create_resources(blocks):
    add_meta_data_to_blocks(blocks)

    actions = []
    for block in blocks:
        process_relations(get_relations(block), actions)

    while actions:
        action = actions.pop()
        result = (
            action.rule.f(action.subj_res)
            if action.src_rel.verb == is_created_as
            else action.rule.f(action.subj_res, action.obj_res)
        )
        if result:
            process_relations(
                _to_list_of_relations(result, action),
                actions,
            )
