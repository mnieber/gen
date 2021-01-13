import typing as T
from dataclasses import dataclass

from moonleap.rel import Rel


@dataclass(frozen=True)
class Prop:
    get_value: T.Callable = None
    set_value: T.Callable = None
    add_value: T.Callable = None
    doc_as_rel: Rel = None
