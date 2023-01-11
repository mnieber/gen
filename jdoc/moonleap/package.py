from jdoc.moonleap.imports import *
from jdoc.moonleap.rule import *


class Package(Entity):
    name: str
    rules: T.List[Rule] = []


class Scope(Entity):
    name: str = ""
    packages: T.List["Package"] = []
