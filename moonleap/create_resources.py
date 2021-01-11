from importlib import import_module

import ramda as R

from moonleap.config import config
from moonleap.parser.term import is_it_term, word_to_term


def _get_verb_that_couples(block, a_term, b_term):
    for line in block.lines:
        state = "find start"
        verb = None
        count_other_terms = 0
        for word in line.words:
            term = word_to_term(word)
            if term and is_it_term(term):
                term = line.it_term

            if term and term == a_term:
                state = "find verb"
            elif word.startswith("/") and state == "find verb":
                verb = word[1:]
                state = "find other term"
            elif (
                word.startswith("/")
                and state == "find other term"
                and count_other_terms > 0
            ):
                state = "find start"
                count_other_terms = 0
            elif state == "find other term" and term and term == b_term:
                return verb
            elif term and state == "find other term":
                count_other_terms += 1

    return None


def derive_resources(resource):
    new_resources = []
    derive_rules = config.get_derive_rules(resource.__class__)
    for derive_rule in derive_rules:
        new_resources += derive_rule(resource)
    return new_resources


def apply_rules(blocks):
    for block in blocks:
        entities = block.get_entities()

        for parent_entity in entities:
            for child_entity in entities:
                if parent_entity is child_entity:
                    continue

                verb = _get_verb_that_couples(
                    block, parent_entity.term, child_entity.term
                )
                if verb:
                    rules = config.get_rules(parent_entity.term.tag)
                    for (object_verb, object_tag), rule in rules:
                        if object_verb == verb and object_tag == child_entity.term.tag:
                            rule(parent_entity, child_entity)


def create_resources(blocks):
    for block in R.sort_by(lambda x: x.level)(blocks):
        parent_blocks = block.get_blocks(include_parents=True, include_self=False)
        child_blocks = block.get_blocks(include_children=True, include_self=False)

        for term in block.get_terms():
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

            entity = create_rule(term, creator_block)
            entity.term = term
            entity.block = creator_block

            creator_block.add_entity(entity)
            if block is not creator_block:
                block.add_entity(entity)

    apply_rules(blocks)
