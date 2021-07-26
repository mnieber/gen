from dataclasses import dataclass

from moonleap import add, tags
from moonleap_tools.pipdependency import PipDependency
from moonleap_project.service import Tool


@dataclass
class Black(Tool):
    pass


@tags(["black"])
def create_black(term, block):
    black = Black(name="black")

    add(black, PipDependency(["black"], is_dev=True))

    return black
