from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    data: str
    tag: str


def maybe_term_to_term(maybe_term):
    if isinstance(maybe_term, Term):
        return maybe_term
    return word_to_term(maybe_term, default_to_tag=True)


def word_to_term(word, default_to_tag=False):
    parts = word.split(":")
    if len(parts) == 2:
        data, tag = parts
        return Term(data or "", tag or "")
    elif default_to_tag:
        return Term(None, word)
    return None


def words_to_terms(words):
    terms = []
    for word in words:
        term = word_to_term(word)
        if term:
            terms.append(term)
    return terms


def term_to_word(term):
    if term.data is None:
        return term.tag
    return f"{term.data}:{term.tag}"


def is_it_term(term):
    return term.tag.lower() in ["it", "its"]
