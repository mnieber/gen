from importlib import import_module

import ramda as R

from moonleap.config import config
from moonleap.parser.term import is_it_term, word_to_term


def _add_child(resource, child_resource):
    if child_resource.__class__ in config.get_child_types(resource.__class__):
        if resource.add_child(child_resource):
            return True
    return False


def _add_parent(resource, parent_resource):
    if parent_resource.__class__ in config.get_parent_types(resource.__class__):
        return resource.add_parent(parent_resource)
    return False


def _are_terms_paired(block, a_term, b_term):
    for line in block.lines:
        state = "find start"
        count_other_terms = 0
        for word in line.words:
            term = word_to_term(word)
            if term and is_it_term(term):
                term = line.it_term

            if term and term == a_term:
                state = "find verb"
            elif word.startswith("/") and state == "find verb":
                state = "find other term"
            elif (
                word.startswith("/")
                and state == "find other term"
                and count_other_terms > 0
            ):
                state = "find start"
                count_other_terms = 0
            elif state == "find other term" and term and term == b_term:
                return True
            elif term and state == "find other term":
                count_other_terms += 1

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

    for parent_resource in resources:
        resources_visible_to_parent_resource = parent_resource.block.get_resources(
            include_parents=True, include_children=True
        )

        for child_resource in resources_visible_to_parent_resource:
            if parent_resource is child_resource:
                continue

            # first check if b is created in a block that describes a
            must_add_child = child_resource.block.describes(parent_resource.term)

            if not must_add_child:
                blocks_visible_to_child_resource = child_resource.block.get_blocks(
                    include_parents=True, include_children=True
                )

                # next, check if there is a block that describes or creates a, and where
                # a and b are paired in the same line in a way that makes a the parent of b
                for block in blocks_visible_to_child_resource:
                    if (
                        block.describes(parent_resource.term)
                        or parent_resource.block is block
                    ):
                        if _are_terms_paired(
                            block, parent_resource.term, child_resource.term
                        ):
                            must_add_child = True
                            break

            if must_add_child:
                result = _add_child(parent_resource, child_resource)
                result = _add_parent(child_resource, parent_resource)


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
