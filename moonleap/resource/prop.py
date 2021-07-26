import typing as T
from dataclasses import dataclass

from moonleap.resource.rel import Rel


@dataclass(frozen=True)
class Prop:
    get_value: T.Callable
    set_value: T.Optional[T.Callable] = None
    rel: T.Optional[Rel] = None
