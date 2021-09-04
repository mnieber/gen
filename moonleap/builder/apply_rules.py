import typing as T

from moonleap.builder.add_resources_to_blocks import _create_resource
from moonleap.parser.block import get_extended_scope_names
from moonleap.parser.term import term_to_word
from moonleap.resource.rel import Forward, Rel
from moonleap.session import get_session
from moonleap.verbs import is_created_as


def _find_or_create_resource(scope, block, term, scope_manager):
    for parent_block in block.get_blocks(include_self=True, include_parents=True):
        resource = parent_block.get_resource(term)
        if resource:
            return resource

    resource = _create_resource(term, block, scope_manager)
    block.add_resource_for_term(resource, term, True)

    for rule in scope.get_rules(is_created_as_rel(term)):
        result = rule.f(resource)
        if result:
            _process_forwards(
                scope, _to_list_of_forward(result, rule), block, scope_manager
            )

    return resource


def _find_term_for_resource(resource, block):
    for parent_block in block.get_blocks(include_parents=True):
        for term, res, is_owner in parent_block.get_resource_by_term():
            if res is resource:
                return term
    return None


def _process_forwards(scope, forwards: T.List[Forward], block, scope_manager):
    for forward in forwards:
        new_obj_resource = forward.obj_res or _find_or_create_resource(
            scope, block, forward.obj, scope_manager
        )
        subj_term = _find_term_for_resource(forward.subj_res, block)
        if subj_term is None:
            raise Exception(
                f"Resource {forward.subj_res} not found in block {block}"
                + "This probably means that a rule made an assumption "
                + "about your spec that doesn't hold true."
            )

        new_rel = Rel(subj_term, forward.verb, forward.obj)
        if not forward.subj_res.has_relation(new_rel, new_obj_resource):
            forward.subj_res.add_relation(new_rel, new_obj_resource)
            _apply_rules(
                new_rel, forward.subj_res, new_obj_resource, block, scope_manager
            )


def _to_list_of_forward(x, rule):
    result = list(x) if (isinstance(x, list) or isinstance(x, tuple)) else [x]
    for forward in result:
        if not isinstance(forward, Forward):
            raise Exception(
                f"A rule ({rule}) should either return a Forward or a list of Forward"
            )
    return result


def _apply_rules(rel, subj_resource, obj_resource, block, scope_manager):
    has_rule = False
    for scope_name in get_extended_scope_names(block):
        scope = scope_manager.get_scope(scope_name)

        for rule in scope.get_rules(rel):
            if rule.fltr_subj and not rule.fltr_subj(subj_resource):
                continue

            if rule.fltr_obj and not rule.fltr_obj(obj_resource):
                continue

            has_rule = True
            result = rule.f(subj_resource, obj_resource)
            if result:
                _process_forwards(
                    scope, _to_list_of_forward(result, rule), block, scope_manager
                )

    return has_rule


def is_created_as_rel(term):
    return Rel(term, is_created_as, term)


def apply_rules(root_block):
    scope_manager = get_session().scope_manager

    for block in root_block.get_blocks(include_children=True):
        for term, resource, is_owner in block.get_resource_by_term():
            if not is_owner:
                continue

            rule = None
            for scope_name in get_extended_scope_names(block):
                scope = scope_manager.get_scope(scope_name)

                for rule in scope.get_rules(is_created_as_rel(term)):
                    result = rule.f(resource)
                    if result:
                        _process_forwards(
                            scope,
                            _to_list_of_forward(result, rule),
                            block,
                            scope_manager,
                        )

            for rel, obj_resource in resource.get_relations():
                if not rel.is_inv:
                    if not _apply_rules(
                        rel, resource, obj_resource, block, scope_manager
                    ):
                        # We should check if the block declared this relation. This
                        # filters out the cases where the relation was added
                        # programatically.
                        if block.has_relation(rel):
                            raise Exception(
                                f"Unmatched relation ({term_to_word(rel.subj)} "
                                + f"{rel.verb} {term_to_word(rel.obj)})"
                                + f" in block: {block}"
                            )
