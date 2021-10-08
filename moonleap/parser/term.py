import typing as T
from dataclasses import dataclass
from fnmatch import fnmatch


@dataclass(frozen=True)
class Term:
    data: T.Optional[str]
    tag: str
    name: T.Optional[str] = None

    def __repr__(self):
        return (
            (self.name + "+" if self.name else "")
            + (self.data + ":" if self.data else "")
            + self.tag
        )


def maybe_term_to_term(maybe_term):
    if isinstance(maybe_term, Term):
        return maybe_term
    return word_to_term(maybe_term, default_to_tag=True)


def word_to_term(word, default_to_tag=False) -> T.Optional[Term]:
    sep_name = word.find("+")
    if sep_name != -1:
        name = word[:sep_name]
        word = word[sep_name + 1 :]
    else:
        name = None

    sep_tag = word.rfind(":")
    if sep_tag != -1:
        tag = word[sep_tag + 1 :]
        data = word[:sep_tag]
    else:
        tag = word
        data = None

    if sep_name == -1 and sep_tag == -1 and not default_to_tag:
        return None

    return Term(data, tag, name)


def words_to_terms(words):
    terms = []
    for word in words:
        term = word_to_term(word)
        if term:
            terms.append(term)
    return terms


def is_it_term(term):
    return term.tag.lower() in ["it", "its"]


def verb_to_word(verb):
    return verb[0] if isinstance(verb, tuple) else verb


def stem_term(term):
    pos = term.tag.find("~")
    return Term(term.data, term.tag[:pos]) if pos != -1 else None


def _match(lhs, rhs):
    if lhs is None or rhs is None:
        return lhs == rhs

    return (
        (lhs == "x" and rhs is not None)
        or (rhs == "x" and lhs is not None)
        or fnmatch(lhs, rhs)
    )


def match_term_to_pattern(term, pattern_term):
    return (
        (pattern_term.data is None or _match(term.data, pattern_term.data))
        and _match(term.tag, pattern_term.tag)
        and _match(term.name, pattern_term.name)
    )
