import typing as T
from dataclasses import dataclass, field
from fnmatch import fnmatch


@dataclass(frozen=True)
class Term:
    data: str
    tag: str
    name: T.Optional[str] = None
    # This field is not used in term comparisons
    is_title: T.Optional[bool] = field(default=False, compare=False)

    def __repr__(self):
        return (
            (self.name + "+" if self.name is not None else "")
            + self.data
            + ":"
            + self.tag
            + ("^" if self.is_title else "")
        )


def word_to_term(word, default_to_tag=False) -> T.Optional[Term]:
    stripped_word = word

    is_title = stripped_word.endswith("^")
    if is_title:
        stripped_word = stripped_word[:-1]

    sep_name = stripped_word.find("+")
    if sep_name != -1:
        name = stripped_word[:sep_name] or ""
        stripped_word = stripped_word[sep_name + 1 :]
    else:
        name = None

    sep_tag = stripped_word.rfind(":")
    if sep_tag != -1:
        tag = stripped_word[sep_tag + len(":") :]
        data = stripped_word[:sep_tag]
    else:
        if not default_to_tag:
            return None
        tag = stripped_word
        data = "x"

    return Term(data, tag, name, is_title)


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
