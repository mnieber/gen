import typing as T
from dataclasses import dataclass


@dataclass(frozen=True)
class MemFun:
    f: T.Callable
