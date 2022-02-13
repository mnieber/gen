import typing as T
from dataclasses import dataclass
from fnmatch import fnmatch


@dataclass(frozen=True)
class Term:
    data: str
    tag: str
    name: T.Optional[str] = None
    stars: T.Optional[int] = 0

    def __repr__(self):
        return (
            (self.name + "+" if self.name is not None else "")
            + self.data
            + ":"
            + self.tag
        )


def maybe_term_to_term(maybe_term):
    if isinstance(maybe_term, Term):
        return maybe_term
    return word_to_term(maybe_term, default_to_tag=True)


def word_to_term(word, default_to_tag=False) -> T.Optional[Term]:
    stars = 0
    if word.endswith("*") or word.endswith("^"):
        stars = 1 if word.endswith("*") else 2
        word = word[:-1]

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
        data = "x"

    if sep_tag == -1 and not default_to_tag:
        return None

    return Term(data, tag, name, stars)


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
    return Term(
        data=term.data, tag=term.tag[:pos] if pos != -1 else term.tag, name=term.name
    )


def _match(lhs, rhs):
    if lhs is None or rhs is None:
        return lhs == rhs

    return lhs == "x" or rhs == "x" or fnmatch(lhs, rhs)


def match_term_to_pattern(term, pattern_term):
    return (
        _match(term.data, pattern_term.data)
        and _match(term.tag, pattern_term.tag)
        and _match(term.name, pattern_term.name)
    )


def named_term(term, name=""):
    if term.name:
        raise Exception("Term already has a name")

    return Term(term.data, term.tag, name=name)


def patch_tag(term, tag):
    return (
        term
        if tag is None
        else Term(data="generic", tag=tag, name=term.name if term else None)
    )
