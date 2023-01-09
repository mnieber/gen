import typing as T
from dataclasses import dataclass, field

from jdoc.packages import *
from jdoc.scenario import *


@dataclass
class Scope(Entity):
    name: str = field(init=False)
    packages: T.List[Package] = field(default_factory=list)


@dataclass
class DefaultScope(Scope):
    def __post_init__(self):
        self.name = "default"


@dataclass
class BackendServiceScope(Scope):
    def __post_init__(self):
        self.name = "backend-service"


class Settings(Entity):
    scope_by_name = {
        "default": DefaultScope(packages=[DefaultPackage()]),
        "backend-service": BackendServiceScope(
            packages=[DefaultPackage(), DjangoPackage()]
        ),
    }


global_settings = Settings()
