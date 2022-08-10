import typing as T

from moonleap.builder.add_meta_data_to_blocks import add_meta_data_to_blocks
from moonleap.builder.create_resource import (
    create_resource_in_block,
    find_describing_block,
)
from moonleap.builder.find_relations import get_relations
from moonleap.packages.rule import Action
from moonleap.parser.term import Term
from moonleap.resource.named_class import NamedResource
from moonleap.resource.rel import Rel
from moonleap.utils.case import kebab_to_camel
from moonleap.verbs import is_created_as


def _find_resource(term, block):
    for parent_block in block.get_blocks(include_self=True, include_parents=True):
        resource = parent_block.get_resource(term)
        if resource:
            return resource
    return None


def _find_rules(rel, subj_res, obj_res):
    rules = []

    for scope in rel.block.get_scopes():
        for rule in scope.find_rules(
            rel,
            subj_base_tags=subj_res.meta.base_tags,
            obj_base_tags=obj_res.meta.base_tags,
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


def _process_relations(relations: T.List[Rel], actions):
    def _find_or_create(rel, term):
        has_name = term.name is not None

        # Step 1: find existing resource
        res = _find_resource(term, rel.block)
        if res:
            return res

        # Step 2: if the resource doesn't exist, find the publishing block. Note that the
        # publishing block may be some child of the current block, and it may be some
        # sibling of the parent block.
        publishing_block = find_describing_block(term, rel.block) or rel.block

        # Step 3: create the resource in the publishing block, and add to current block
        res = create_resource_in_block(term, publishing_block)
        if rel.block is not publishing_block:
            rel.block.add_resource_for_term(res, term, False)

        # Step 4: if a resource appears in the heading of the publishing block, then we add
        # it to its parent block as well. In other words, a parent block knows
        # about any resource that is described in its child blocks.
        # Note that this creates a symmetry between finding resources and creating
        # them: the blocks that are "competing" for creating the resource are the same
        # blocks where the resource can be found if it already existed.
        if publishing_block.describes(term) and publishing_block.parent_block:
            publishing_block.parent_block.add_resource_for_term(res, term, False)

        # Step 5: handle named term
        if has_name:
            assert isinstance(res, NamedResource)
            res.name = kebab_to_camel(term.name)
            res.typ = _find_or_create(
                rel, Term(data=term.data, tag=term.tag, is_title=term.is_title)
            )

        # Step 6: process the is_created_as relation
        _process_relations(
            [Rel(term, is_created_as, term, publishing_block, rel.origin)], actions
        )

        return res

    for rel in relations:
        rel.block.register_relation(rel)

        subj_res = _find_or_create(rel, rel.subj)
        obj_res = _find_or_create(rel, rel.obj)

        if not subj_res.has_relation(rel, obj_res):
            subj_res.add_relation(rel, obj_res)

            rules = _find_rules(rel, subj_res, obj_res)
            if not rules and rel.verb != is_created_as:
                raise Exception(f"Unmatched relation ({rel}) in block: {rel.block}")

            for rule in rules:
                _add_action(actions, Action(rule, rel, subj_res, obj_res))


def create_resources(blocks):
    add_meta_data_to_blocks(blocks)

    actions = []
    for block in blocks:
        _process_relations(get_relations(block), actions)

    while actions:
        action = actions.pop()
        result = (
            action.rule.f(action.subj_res)
            if action.src_rel.verb == is_created_as
            else action.rule.f(action.subj_res, action.obj_res)
        )
        if result:
            _process_relations(
                _to_list_of_relations(result, action),
                actions,
            )
