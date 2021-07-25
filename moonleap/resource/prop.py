import typing as T
from dataclasses import dataclass


@dataclass(frozen=True)
class Prop:
    get_value: T.Callable = None
    set_value: T.Callable = None
    add_value: T.Callable = None
