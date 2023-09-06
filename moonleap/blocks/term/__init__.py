import typing as T
from dataclasses import dataclass, field
from fnmatch import fnmatch


@dataclass(frozen=True)
class Term:
    parts: T.Tuple[str]
    name: T.Optional[str] = None
    # This field is not used in term comparisons
    is_title: T.Optional[bool] = field(default=False, compare=False)

    @property
    def data(self):
        return ":".join(self.parts[:-1])

    @property
    def tag(self):
        return self.parts[-1]

    def __repr__(self):
        return (
            (self.name + "+" if self.name is not None else "")
            + ":".join(self.parts)
            + ("^" if self.is_title else "")
        )


def str_to_term(word, default_to_tag=False) -> T.Optional[Term]:
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
    if sep_tag == -1:
        if not default_to_tag:
            return None
        parts = ["x", stripped_word]
    else:
        parts = []
        while sep_tag != -1:
            part = stripped_word[sep_tag + len(":") :]
            parts.insert(0, part)
            stripped_word = stripped_word[:sep_tag]
            sep_tag = stripped_word.rfind(":")
        parts.insert(0, stripped_word)

    return Term(tuple(parts), name, is_title)


def strs_to_terms(strs):
    terms = []
    for s in strs:
        term = str_to_term(s)
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
    if len(term.parts) != len(pattern_term.parts):
        return False

    for i in range(len(term.parts)):
        if not _match(term.parts[i], pattern_term.parts[i]):
            return False

    return _match(term.name, pattern_term.name)


def named_term(term, name=""):
    if term.name:
        raise Exception("Term already has a name")

    return Term(term.parts, name=name)


def unnamed_term(term):
    return Term(parts=term.parts, is_title=term.is_title)


def patch_tag(term, tag):
    return (
        term
        if tag is None
        else Term(parts=("generic", tag), name=term.name if term else None)
    )
