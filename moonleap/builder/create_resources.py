import ramda as R
from moonleap.builder.config import config
from moonleap.parser.term import is_it_term, word_to_term
from moonleap.resource import Resource
from moonleap.resource.rel import Rel
from moonleap.verbs import is_created_as


def add_relations(lhs_terms, verb, terms, result):
    for lhs_term in lhs_terms:
        for term in terms:
            result.append(Rel(subj=lhs_term, verb=verb, obj=term))


def _process_words(words, it_term, result, word_idx=0):
    first_term = None
    lhs_terms = []
    verb = None
    terms = []

    while word_idx < len(words):
        word = words[word_idx]
        term = None

        if word == "(":
            term, word_idx = _process_words(words, it_term, result, word_idx + 1)

        if word == ")":
            word_idx += 1
            break

        if term is None:
            term = word_to_term(word)

        if term:
            if is_it_term(term):
                term = it_term

            if not first_term:
                first_term = term

            terms.append(term)

        if word.startswith("/"):
            if verb:
                add_relations(lhs_terms, verb, terms, result)
            verb = word[1:]
            lhs_terms = terms
            terms = []

        word_idx += 1

    add_relations(lhs_terms, verb, terms, result)
    return first_term, word_idx


def _get_relations(block):
    result = []
    for line in block.lines:
        _process_words(line.words, line.it_term, result)

    return result


def derive_resources(resource):
    new_resources = []
    derive_rules = config.get_derive_rules(resource.__class__)
    for derive_rule in derive_rules:
        new_resources += derive_rule(resource)
    return new_resources


def find_relations(blocks):
    for block in blocks:
        for rel in _get_relations(block):
            parent_resource = block.get_resource(rel.subj)
            child_resource = block.get_resource(rel.obj)
            if parent_resource and child_resource:
                parent_resource.add_relation(
                    rel,
                    child_resource,
                )


def apply_rules(blocks):
    root_block = blocks[0]
    for parent_resource in root_block.get_resources(include_children=True):
        for rule in config.get_rules(
            Rel(parent_resource.term, is_created_as, parent_resource.term),
            parent_resource,
            parent_resource,
        ):
            rule.f(parent_resource)
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
            if block.get_resource(term):
                continue

            resource = None

            for parent_block in parent_blocks:
                resource = parent_block.get_resource(term)
                if resource:
                    block.add_resource(resource)
                    break

            if resource:
                continue

            creator_block = block
            if not block.describes(term):
                for child_block in child_blocks:
                    if child_block.describes(term):
                        creator_block = child_block
                        break

            create_rule = config.get_create_rule(term) or _create_generic_resource
            resource = create_rule(term, creator_block)
            resource.term = term
            resource.block = creator_block

            creator_block.add_resource(resource)
            if block is not creator_block:
                block.add_resource(resource)

            # If a resource appears in the heading of the creator block, then we add it to
            # it's parent block as well. In other words, a parent block knows about any resource
            # that is described in its child blocks.
            if creator_block.describes(term):
                if (
                    creator_block.parent_block
                    and not creator_block.parent_block.get_resource(term)
                ):
                    creator_block.parent_block.add_resource(resource)

    find_relations(blocks)
    apply_rules(blocks)
