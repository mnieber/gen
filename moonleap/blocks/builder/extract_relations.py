from moonleap.blocks.term import is_it_term, str_to_term
from moonleap.resources.relations.rel import Rel


def _add_relations(block, lhs_terms, verb, terms, result):
    for lhs_term in lhs_terms:
        for term in terms:
            result.append(Rel(subj=lhs_term, verb=verb, obj=term, block=block))


def _process_words(block, words, it_term, result, word_idx=0):
    first_term = None
    lhs_terms = []
    verb = None
    terms = []

    while word_idx < len(words):
        word = words[word_idx]
        term = None

        if word == "(":
            term, word_idx = _process_words(block, words, it_term, result, word_idx + 1)

        if word == ")":
            break

        if term is None:
            term = str_to_term(word)

        if term:
            if is_it_term(term):
                term = it_term

            if not first_term:
                first_term = term

            terms.append(term)

        if word.startswith("/"):
            if verb:
                _add_relations(block, lhs_terms, verb, terms, result)
            verb = word[1:]
            lhs_terms = terms
            terms = []

        word_idx += 1

    _add_relations(block, lhs_terms, verb, terms, result)
    return first_term, word_idx


def extract_relations(block):
    result = []
    for line in block.lines:
        _process_words(block, line.words, line.it_term, result)

    return result
