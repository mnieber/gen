import typing as T
from dataclasses import dataclass
from fnmatch import fnmatch

from moonleap.parser.term import Term, word_to_term
from moonleap.utils import maybe_tuple_to_tuple


@dataclass(frozen=True)
class Rel:
    subj: T.Optional[Term] = None
    verb: T.Optional[T.Union[str, T.Tuple[str, ...]]] = None
    obj: T.Optional[Term] = None
    is_inv: bool = False

    def inv(self):
        return Rel(verb=self.verb, obj=self.obj, subj=self.subj, is_inv=not self.is_inv)


def _is_intersecting(lhs, rhs):
    lhs = maybe_tuple_to_tuple(lhs)
    rhs = maybe_tuple_to_tuple(rhs)

    for x in lhs:
        if x in rhs:
            return True
    return False


def _match_term_to_pattern(term, pattern_term):
    datas_match = pattern_term.data is None or fnmatch(
        term.data or "", pattern_term.data
    )
    tags_match = fnmatch(term.tag, pattern_term.tag)
    return datas_match and tags_match


def fuzzy_match(input_rel, pattern_rel):
    return (
        input_rel.is_inv == pattern_rel.is_inv
        and _is_intersecting(input_rel.verb, pattern_rel.verb)
        and _match_term_to_pattern(input_rel.obj, pattern_rel.obj)
        and (
            pattern_rel.subj is None
            or (
                input_rel.subj
                and _match_term_to_pattern(input_rel.subj, pattern_rel.subj)
            )
        )
    )


@dataclass
class Forward:
    rel: Rel
    subj_res: T.Any = None
    obj_res: T.Any = None


def _to_term(x: T.Union[object, Term, str]) -> Term:
    if isinstance(x, str):
        return word_to_term(x)

    if isinstance(x, Term):
        return x

    return T.cast(T.Any, x).term


def create_forward(
    subj: T.Union[object, Term, str],
    verb: T.Union[str, T.Tuple[str, ...]],
    obj: T.Union[object, Term, str],
    subj_res: T.Any = None,
    obj_res: T.Any = None,
):
    return Forward(Rel(_to_term(subj), verb, _to_term(obj)), subj_res, obj_res)
