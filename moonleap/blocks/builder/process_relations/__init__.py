import typing as T

from moonleap.blocks.term import Term
from moonleap.blocks.verbs import is_created_as
from moonleap.packages.rule import Action
from moonleap.resources.named_resource import NamedResource
from moonleap.resources.relations.rel import Rel
from moonleap.utils.case import kebab_to_camel

from .create_resource_in_block import create_resource_in_block, find_describing_block


def process_relations(relations: T.List[Rel], actions):
    def _find_or_create(rel, term):
        has_name = term.name is not None

        # Step 1: find existing resource
        res = _find_resource(term, rel.block)
        if res:
            return res

        # Step 2: if the resource doesn't exist, find the publishing block. Note that the
        # publishing block may be some child of the current block, some parent of the current block
        # or some sibling of some parent block.
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
        process_relations(
            [
                Rel(
                    subj=term,
                    verb=is_created_as,
                    obj=term,
                    block=publishing_block,
                    origin=rel.origin,
                )
            ],
            actions,
        )

        return res

    for rel in relations:
        rel.block.register_relation(rel)

        if not rel.subj_res:
            rel.subj_res = _find_or_create(rel, rel.subj)

        if not rel.obj_res:
            rel.obj_res = _find_or_create(rel, rel.obj)

        if not rel.subj_res.has_relation(rel, rel.obj_res):
            rel.subj_res.add_relation(rel, rel.obj_res)

            rules = _find_rules(rel)
            if not rules and rel.verb != is_created_as:
                raise Exception(f"Unmatched relation ({rel}) in block: {rel.block}")

            for rule in rules:
                _add_action(actions, Action(rule, rel))


def _find_resource(term, block):
    for parent_block in block.get_blocks(include_self=True, include_parents=True):
        resource = parent_block.get_resource(term)
        if resource:
            return resource
    return None


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