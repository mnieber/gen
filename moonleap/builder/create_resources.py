import ramda as R
from moonleap.builder.config import config
from moonleap.parser.term import is_it_term, word_to_term
from moonleap.resource import Resource
from moonleap.resource.rel import Forward, Rel
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


def _find_or_create_resource(block, term):
    for parent_block in block.get_blocks(include_self=True, include_parents=True):
        resource = parent_block.get_resource(term)
        if resource:
            return resource
    resource = _create_resource(term, block)
    block.add_resource(resource)
    return resource


def _process_forwards(forwards: [Forward], block):
    for forward in forwards:
        new_rel = forward.rel
        new_parent_resource = forward.subj_res or _find_or_create_resource(
            block, new_rel.subj
        )
        new_child_resource = forward.obj_res or _find_or_create_resource(
            block, new_rel.obj
        )

        if not new_parent_resource.has_relation(new_rel, new_child_resource):
            new_parent_resource.add_relation(new_rel, new_child_resource)
            _apply_rules(
                new_rel,
                new_parent_resource,
                new_child_resource,
            )


def _to_list_of_forward(x, rule):
    result = x if (isinstance(x, list) or isinstance(x, tuple)) else [x]
    for forward in result:
        if not isinstance(forward, Forward):
            raise Exception(
                f"A rule ({rule}) should either return a Forward or a list of Forward"
            )
    return result


def _apply_rules(rel, parent_resource, child_resource):
    if rel.is_inv:
        return

    block = (
        child_resource.block
        if child_resource.block
        in parent_resource.block.get_blocks(include_children=True)
        else parent_resource.block
    )

    for rule in config.get_rules(rel):
        if rule.fltr_subj and not rule.fltr_subj(parent_resource):
            continue

        if rule.fltr_obj and not rule.fltr_obj(child_resource):
            continue

        result = rule.f(parent_resource, child_resource)
        if result:
            _process_forwards(_to_list_of_forward(result, rule), block)


def apply_rules(blocks):
    root_block = blocks[0]
    for parent_resource in root_block.get_resources(include_children=True):

        is_created_as_rel = Rel(
            parent_resource.term, is_created_as, parent_resource.term
        )
        for rule in config.get_rules(is_created_as_rel):
            result = rule.f(parent_resource)
            if result:
                _process_forwards(
                    _to_list_of_forward(result, rule), parent_resource.block
                )

        for rel, child_resource in parent_resource.get_relations():
            _apply_rules(rel, parent_resource, child_resource)


def _create_generic_resource(term, block):
    resource = Resource()
    resource.term = term
    resource.block = block
    return resource


def _create_resource(term, creator_block):
    create_rule = config.get_create_rule(term) or _create_generic_resource
    resource = create_rule(term, creator_block)
    resource.term = term
    resource.block = creator_block
    return resource


def add_resources_to_blocks(blocks):
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

            resource = _create_resource(term, creator_block)
            creator_block.add_resource(resource)
            if block is not creator_block:
                block.add_resource(resource)

            # If a resource appears in the heading of the creator block, then we add
            # it to it's parent block as well. In other words, a parent block knows
            # about any resource that is described in its child blocks.
            if creator_block.describes(term):
                if (
                    creator_block.parent_block
                    and not creator_block.parent_block.get_resource(term)
                ):
                    creator_block.parent_block.add_resource(resource)


def create_resources(blocks):
    add_resources_to_blocks(blocks)
    find_relations(blocks)
    apply_rules(blocks)
