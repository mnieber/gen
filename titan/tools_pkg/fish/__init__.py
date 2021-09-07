from dataclasses import dataclass

from moonleap import add, create, rule
from moonleap.verbs import uses
from titan.project_pkg.service import Tool
from titan.tools_pkg.pkgdependency import PkgDependency

from . import opt_paths


@dataclass
class Fish(Tool):
    pass


@rule("service", uses, "fish")
def service_has_fish(service, fish):
    service.shell = "fish"


@create("fish", ["tool"])
def create_fish(term, block):
    fish = Fish(name="fish")

    add(fish, PkgDependency(["fish"], is_dev=True))
    add(fish, opt_paths.fish_opt_path)

    return fish
