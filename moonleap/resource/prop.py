import typing as T
from dataclasses import dataclass


@dataclass(frozen=True)
class Prop:
    get_value: T.Callable
    set_value: T.Optional[T.Callable] = None
