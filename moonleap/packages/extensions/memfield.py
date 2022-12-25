import typing as T
from dataclasses import dataclass


@dataclass(frozen=True)
class MemField:
    f: T.Any
