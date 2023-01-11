from jdoc.moonleap.imports import *
from jdoc.moonleap.package import *
from jdoc.moonleap.rule import *


class Line(Entity):
    terms: T.List[str] = []


class Block(Entity):
    name: str = ""
    lines: list[Line] = []
    relations: list[Relation] = []
    scopes: list[Scope] = []
