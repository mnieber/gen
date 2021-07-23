import typing as T
from dataclasses import dataclass, field

from moonleap.resource.rel import Rel


@dataclass(frozen=True)
class Prop:
    get_value: T.Callable = None
    set_value: T.Callable = None
    add_value: T.Callable = None
