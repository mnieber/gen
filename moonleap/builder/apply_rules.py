import typing as T

from moonleap.builder.add_resources_to_blocks import create_resource_and_add_to_block
from moonleap.parser.term import term_to_word
from moonleap.resource.forward import to_list_of_relations
from moonleap.resource.rel import Rel
from moonleap.verbs import is_created_as


def _find_resource(term, block):
    for parent_block in block.get_blocks(include_self=True, include_parents=True):
        resource = parent_block.get_resource(term)
        if resource:
            return resource
    return None


def _find_rules(rel, subj_res, obj_res, block):
    rules = []

    for scope in block.scopes:
        for rule in scope.find_rules(
            rel,
            subj_base_tags=subj_res._meta.base_tags,
            obj_base_tags=obj_res._meta.base_tags,
        ):
            rules.append(rule)

    return rules


def _add_rule_tuple(rule_tuples, rule_tuple):
    p = rule_tuple[0].priority
    for i in range(len(rule_tuples)):
        if rule_tuples[i][0].priority >= p:
            rule_tuples.insert(i, rule_tuple)
            break
    else:
        rule_tuples.append(rule_tuple)


def _find_or_create_resource(term, block):
    res = _find_resource(term, block)
    return (res, None) if res else create_resource_and_add_to_block(term, block)


def _process_relations(relations: T.List[Rel], block, rule_tuples):
    for rel in relations:
        if rel.verb != is_created_as:
            block.register_relation(rel)

        subj_res, forward = _find_or_create_resource(rel.subj, block)
        if forward:
            _process_relations([forward], subj_res._meta.block, rule_tuples)

        obj_res, forward = _find_or_create_resource(rel.obj, block)
        if forward:
            _process_relations([forward], obj_res._meta.block, rule_tuples)

        if not subj_res.has_relation(rel, obj_res):
            subj_res.add_relation(rel, obj_res)

            rules = _find_rules(rel, subj_res, obj_res, block)
            if not rules:
                # We should check if the block declared this relation. This
                # filters out the cases where the relation was added
                # programatically.
                if block.has_relation(rel):
                    raise Exception(
                        f"Unmatched relation ({term_to_word(rel.subj)} "
                        + f"/{rel.verb} {term_to_word(rel.obj)}) in block: {block}"
                    )

            for rule in rules:
                _add_rule_tuple(rule_tuples, (rule, rel, subj_res, obj_res, block))


def apply_rules(lists_of_relations):
    rule_tuples = []
    for list_of_relations, block in lists_of_relations:
        _process_relations(list_of_relations, block, rule_tuples)

    while rule_tuples:
        rule_tuple = rule_tuples.pop()
        (rule, rel, subj_res, obj_res, block) = rule_tuple
        result = (
            rule.f(subj_res) if rel.verb == is_created_as else rule.f(subj_res, obj_res)
        )
        if result:
            _process_relations(to_list_of_relations(result, rule), block, rule_tuples)
