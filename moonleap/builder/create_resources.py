import typing as T

from moonleap.builder.add_meta_data_to_blocks import add_meta_data_to_blocks
from moonleap.builder.create_resource import create_resource_and_add_to_block
from moonleap.builder.find_relations import get_relations
from moonleap.builder.rule import Action
from moonleap.builder.scope import get_base_tags
from moonleap.parser.term import Term
from moonleap.resource.named_class import NamedResource
from moonleap.resource.rel import Rel
from moonleap.utils.case import kebab_to_camel
from moonleap.verbs import is_created_as, uses


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
            subj_base_tags=get_base_tags(subj_res),
            obj_base_tags=get_base_tags(obj_res),
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
        res = _find_resource(term, rel.block)
        if not res:
            res, creator_block = create_resource_and_add_to_block(term, rel.block)
            _process_relations(
                [Rel(term, is_created_as, term, creator_block, rel.origin)], actions
            )
            if isinstance(res, NamedResource):
                res.name = kebab_to_camel(term.name)
                res.typ = _find_or_create(rel, Term(data=term.data, tag=term.tag))

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
