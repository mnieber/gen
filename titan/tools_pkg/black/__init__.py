from dataclasses import dataclass

from moonleap import add, create
from titan.tools_pkg.pipdependency import PipDependency
from titan.project_pkg.service import Tool


@dataclass
class Black(Tool):
    pass


@create(["black"])
def create_black(term, block):
    black = Black(name="black")

    add(black, PipDependency(["black"], is_dev=True))

    return black
