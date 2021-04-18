from dataclasses import dataclass

from moonleap import add, rule, tags
from moonleap.verbs import uses
from moonleap_tools.pkgdependency import PkgDependency
from moonleap_tools.tool import Tool

from . import opt_paths


@dataclass
class Fish(Tool):
    pass


@rule("service", uses, "fish")
def service_has_fish(service, fish):
    service.shell = "fish"


@tags(["fish"])
def create_fish(term, block):
    fish = Fish()

    add(fish, PkgDependency(["fish"], is_dev=True))
    add(fish, opt_paths.fish_opt_path)

    return fish
