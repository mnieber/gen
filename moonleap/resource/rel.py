import typing as T
from dataclasses import dataclass
from fnmatch import fnmatch

from moonleap.parser.term import Term
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


def _patch_tag(term, tag):
    return term if tag is None else Term(data=None, tag=tag)


def fuzzy_match(input_rel, pattern_rel, subj_base_tags, obj_base_tags):
    for obj_base_tag in [None, *obj_base_tags]:
        for subj_base_tag in [None, *subj_base_tags]:
            rel = Rel(
                subj=_patch_tag(input_rel.subj, subj_base_tag),
                verb=input_rel.verb,
                is_inv=input_rel.is_inv,
                obj=_patch_tag(input_rel.obj, obj_base_tag),
            )
            if (
                rel.is_inv == pattern_rel.is_inv
                and _is_intersecting(rel.verb, pattern_rel.verb)
                and _match_term_to_pattern(rel.obj, pattern_rel.obj)
                and (
                    pattern_rel.subj is None
                    or (rel.subj and _match_term_to_pattern(rel.subj, pattern_rel.subj))
                )
            ):
                return True
    return False
