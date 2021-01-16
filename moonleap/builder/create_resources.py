import ramda as R
from moonleap.builder.config import config
from moonleap.parser.term import is_it_term, word_to_term
from moonleap.resource import Resource
from moonleap.resource.rel import Rel


def _get_verbs_that_couple(block, a_term, b_term):
    result = []
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
                result.append(verb)
            elif term and state == "find other term":
                count_other_terms += 1

    return result


def derive_resources(resource):
    new_resources = []
    derive_rules = config.get_derive_rules(resource.__class__)
    for derive_rule in derive_rules:
        new_resources += derive_rule(resource)
    return new_resources


def find_relations(blocks):
    for block in blocks:
        entities = block.get_entities()

        for parent_resource in entities:
            for child_resource in entities:
                if parent_resource is child_resource:
                    continue

                for verb in _get_verbs_that_couple(
                    block, parent_resource.term, child_resource.term
                ):
                    rel = Rel(
                        subj=parent_resource.term,
                        verb=verb,
                        obj=child_resource.term,
                    )
                    parent_resource.add_relation(
                        rel,
                        child_resource,
                    )


def apply_rules(blocks):
    root_block = blocks[0]
    for parent_resource in root_block.get_entities(include_children=True):
        for rel, child_resource in parent_resource.get_relations():
            if rel.is_inv:
                continue

            for rule in config.get_rules(rel, parent_resource, child_resource):
                rule.f(parent_resource, child_resource)


def _create_generic_resource(term, block):
    resource = Resource()
    resource.term = term
    resource.block = block
    return resource


def create_resources(blocks):
    for block in R.sort_by(lambda x: x.level)(blocks):
        parent_blocks = block.get_blocks(include_parents=True, include_self=False)
        child_blocks = block.get_blocks(include_children=True, include_self=False)

        for term in block.get_terms():
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

            create_rule = config.get_create_rule(term) or _create_generic_resource
            entity = create_rule(term, creator_block)
            entity.term = term
            entity.block = creator_block

            creator_block.add_entity(entity)
            if block is not creator_block:
                block.add_entity(entity)

    find_relations(blocks)
    apply_rules(blocks)
