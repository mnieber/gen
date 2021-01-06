from importlib import import_module

import ramda as R

from moonleap.config import config
from moonleap.parser.term import word_to_term


def _add_child(resource, child_resource):
    if child_resource.__class__ in config.get_child_types(resource.__class__):
        if resource.add_child(child_resource):
            return True
    return False


def _add_parent(resource, parent_resource):
    if parent_resource.__class__ in config.get_parent_types(resource.__class__):
        return resource.add_parent(parent_resource)
    return False


def _are_terms_paired(block, term, other_resource):
    for line in block.lines:
        state = "find start"
        count_other_resources = 0
        for word in line.words:
            term = word_to_term(word)

            if term and term == term:
                state = "find verb"
            elif word.startswith("/") and state == "find verb":
                state = "find other resource"
            elif (
                word.startswith("/")
                and state == "find other resource"
                and count_other_resources > 0
            ):
                state = "find start"
                count_other_resources = 0
            elif state == "find other resource" and term and term == other_term:
                return True
            elif term and state == "find other resource":
                count_other_resources += 1

    return False


def derive_resources(resource):
    new_resources = []
    derive_rules = config.get_derive_rules(resource.__class__)
    for derive_rule in derive_rules:
        new_resources += derive_rule(resource)
    return new_resources


def add_resource(block, resource, term):
    block.add_resource(resource, term)

    for new_resource in derive_resources(resource):
        add_resource(block, new_resource, term)


def group_resources(blocks):
    resources = blocks[0].get_resources(include_children=True)

    for a_resource in resources:
        for b_resource in resources:
            if a_resource is b_resource:
                continue

            # first check if b is created in a block that describes a
            must_add_child = b_resource.block.describes(a_resource.term)

            if not must_add_child:
                # next, check if there is a block that describes or creates a, and where
                # a and b are paired in the same line in a way that makes a the parent of b
                for block in blocks:
                    if block.describes(a_resource.term) or a_resource.block is block:
                        if _are_terms_paired(block, a_resource.term, b_resource.term):
                            must_add_child = True
                            break

            if must_add_child:
                result = _add_child(a_resource, b_resource)
                result = _add_parent(b_resource, a_resource)


def create_resources(blocks):
    for block in R.sort_by(lambda x: -1 * x.level)(blocks):
        for term in reversed(block.get_terms()):
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if term in block.get_terms(include_parents=True, include_self=False):
                # term will be processed by a parent block
                continue

            for resource in create_rule(term, block):
                if resource:
                    add_resource(block, resource, term)

    group_resources(blocks)
