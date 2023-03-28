import typing as T

from jdoc.moonleap.imports import *
from jdoc.moonleap.package import *
from jdoc.moonleap.rule import *


class Line(Entity):
    terms: T.List[str] = []


class Block(Entity):
    name: str = ""
    lines: T.List[Line] = []
    relations: T.List[Relation] = []
    scopes: T.List[Scope] = []
