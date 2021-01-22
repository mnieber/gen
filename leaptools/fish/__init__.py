from dataclasses import dataclass

from leaptools.pkgdependency import PkgDependency
from leaptools.tool import Tool
from moonleap import add, rule, tags
from moonleap.verbs import uses


@dataclass
class Fish(Tool):
    pass


@rule("service", uses, "fish")
def service_has_fish(service, fish):
    service.add_tool(fish)
    service.shell = "fish"


@tags(["fish"])
def create_fish(term, block):
    fish = Fish()

    add(fish, PkgDependency(["fish"], is_dev=True))

    return fish
