import typing as T
from dataclasses import dataclass, field

from moonleap.block_builder.block import Block
from moonleap.spec.term import Term, match_term_to_pattern, patch_tag
from moonleap.utils import maybe_tuple_to_tuple


@dataclass
class Rel:
    subj: T.Optional[Term] = None
    subj_res: T.Optional["Resource"] = None
    verb: T.Optional[T.Union[str, T.Tuple[str, ...]]] = None
    obj: T.Optional[Term] = None
    block: T.Optional[Block] = None
    obj_res: T.Optional["Resource"] = None

    # This field is used for debugging purposes. It allows us to trace the chain of
    # action --(src_rel)--> relation --(origin)--> action etc, so we can figure out
    # why a certain rule was triggered.
    origin: T.Optional[T.Any] = field(default_factory=lambda: None, repr=False)

    def __repr__(self):
        verb = f"{self.verb[0]}*" if isinstance(self.verb, tuple) else self.verb
        return f"Rel({self.subj} /{verb} {self.obj})"

    def trace(self):
        if self.origin and hasattr(self.origin, "trace"):
            self.origin.trace()
        else:
            print(f"{self} in {self.block}")


def _is_intersecting(lhs, rhs):
    lhs = maybe_tuple_to_tuple(lhs)
    rhs = maybe_tuple_to_tuple(rhs)

    for x in lhs:
        if x in rhs:
            return True
    return False


def fuzzy_match(input_rel, pattern_rel, subj_base_tags, obj_base_tags):
    for obj_base_tag in [None, *obj_base_tags]:
        for subj_base_tag in [None, *subj_base_tags]:
            rel = Rel(
                subj=patch_tag(input_rel.subj, subj_base_tag),
                verb=input_rel.verb,
                obj=patch_tag(input_rel.obj, obj_base_tag),
            )
            if (
                _is_intersecting(rel.verb, pattern_rel.verb)
                and match_term_to_pattern(rel.obj, pattern_rel.obj)
                and (
                    pattern_rel.subj is None
                    or match_term_to_pattern(rel.subj, pattern_rel.subj)
                )
            ):
                return True
    return False
