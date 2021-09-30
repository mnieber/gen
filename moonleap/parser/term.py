import typing as T
from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    data: T.Optional[str]
    tag: str

    def __repr__(self):
        return f"{self.data}:{self.tag}"


def maybe_term_to_term(maybe_term):
    if isinstance(maybe_term, Term):
        return maybe_term
    return word_to_term(maybe_term, default_to_tag=True)


def word_to_term(word, default_to_tag=False) -> T.Optional[Term]:
    parts = word.split(":")
    if len(parts) >= 2:
        data, tag = ":".join(parts[:-1]), parts[-1]
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


def verb_to_word(verb):
    return verb[0] if isinstance(verb, tuple) else verb


def is_generic_term(term):
    return term.data == "x" or term.tag == "x"


def create_generic_terms(term):
    return [Term(term.data, "x"), Term("x", term.tag)]


def stem_term(term):
    pos = term.tag.find("~")
    return Term(term.data, term.tag[:pos]) if pos != -1 else None
