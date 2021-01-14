from dataclasses import dataclass
from fnmatch import fnmatch

from moonleap.utils import maybe_tuple_to_tuple


@dataclass(frozen=True)
class Term:
    data: str
    tag: str


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


def match_term_to_pattern(term, pattern_term):
    datas_match = pattern_term.data is None or fnmatch(
        term.data or "", pattern_term.data
    )
    tags_match = fnmatch(term.tag, pattern_term.tag)
    return datas_match and tags_match


def _is_intersecting(lhs, rhs):
    lhs = maybe_tuple_to_tuple(lhs)
    rhs = maybe_tuple_to_tuple(rhs)

    for x in lhs:
        if x in rhs:
            return True
    return False


def fuzzy_match(input_rel, pattern_rel):
    return (
        input_rel.is_inv == pattern_rel.is_inv
        and _is_intersecting(input_rel.verb, pattern_rel.verb)
        and match_term_to_pattern(input_rel.obj, pattern_rel.obj)
        and (
            pattern_rel.subj is None
            or (
                input_rel.subj
                and match_term_to_pattern(input_rel.subj, pattern_rel.subj)
            )
        )
    )
