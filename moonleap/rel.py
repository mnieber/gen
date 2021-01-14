import typing as T
from dataclasses import dataclass

from moonleap.parser.term import Term


@dataclass(frozen=True)
class Rel:
    subj: Term = None
    verb: T.Union[str, T.Tuple[str]] = None
    obj: Term = None
    is_inv: bool = False

    def inv(self):
        return Rel(verb=self.verb, obj=self.obj, subj=self.subj, is_inv=not self.is_inv)
