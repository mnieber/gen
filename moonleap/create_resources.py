from importlib import import_module

import ramda as R

from moonleap.config import config
from moonleap.entity import Entity
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
    for block in blocks:
        entities = block.get_entities()

        for parent_entity in entities:
            for child_entity in entities:
                if parent_entity is child_entity:
                    continue

                must_add_child = block.describes(
                    parent_entity.term
                ) or _are_terms_paired(block, parent_entity.term, child_entity.term)

                if must_add_child:
                    for parent_resource in parent_entity.resources:
                        for child_resource in child_entity.resources:
                            _add_child(parent_resource, child_resource)
                            _add_parent(child_resource, parent_resource)


def create_resources(blocks):
    for block in R.sort_by(lambda x: x.level)(blocks):
        parent_blocks = block.get_blocks(include_parents=True, include_self=False)
        child_blocks = block.get_blocks(include_children=True, include_self=False)

        for term in reversed(block.get_terms()):
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if block.get_entity(term):
                continue

            entity = None

            for parent_block in parent_blocks:
                entity = parent_block.get_entity(term)
                if entity:
                    block.add_entity(entity)
                    break

            if entity:
                continue

            creator_block = block
            if not block.describes(term):
                for child_block in child_blocks:
                    if child_block.describes(term):
                        creator_block = child_block
                        break

            entity = Entity(creator_block, term, create_rule(term, creator_block))
            creator_block.add_entity(entity)
            if block is not creator_block:
                block.add_entity(entity)

    group_resources(blocks)
