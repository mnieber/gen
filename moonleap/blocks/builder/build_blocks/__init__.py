from moonleap.blocks.builder.process_relations import process_relations
from moonleap.blocks.verbs import _is_created_as
from moonleap.resources.relations.rel import Rel

from .add_meta_data_to_blocks import add_meta_data_to_blocks
from .extract_relations import extract_relations


def _to_list_of_relations(x, action):
    result = list(x) if (isinstance(x, list) or isinstance(x, tuple)) else [x]
    for rel in result:
        if not isinstance(rel, Rel):
            raise Exception(
                f"A rule ({action.rule}) should either return a Rel or a list of Rel"
            )
    return [
        Rel(
            subj=x.subj,
            subj_res=x.subj_res,
            verb=x.verb,
            obj=x.obj,
            obj_res=x.obj_res,
            block=x.block or action.src_rel.block,
            origin=action,
        )
        for x in result
    ]


def build_blocks(blocks):
    add_meta_data_to_blocks(blocks)

    actions = []
    for block in blocks:
        process_relations(extract_relations(block), actions)

    next_actions = actions
    while next_actions:
        actions_to_retry = []
        nr_actions = len(next_actions)

        while next_actions:
            action = next_actions.pop()
            result = (
                action.rule.f(action.src_rel.subj_res)
                if action.src_rel.verb == _is_created_as
                else action.rule.f(action.src_rel.subj_res, action.src_rel.obj_res)
            )
            if result == "retry":
                actions_to_retry.append(action)
                continue

            if result:
                process_relations(
                    _to_list_of_relations(result, action),
                    actions,
                )

        next_actions = actions_to_retry
        if len(next_actions) == nr_actions:
            raise Exception("Infinite loop in build_blocks")
