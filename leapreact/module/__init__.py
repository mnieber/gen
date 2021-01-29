from dataclasses import dataclass

from leapreact.reacttool import ReactTool
from moonleap import MemFun, extend, tags

from .render import render_module


@dataclass
class Module(ReactTool):
    name: str


@tags(["module"])
def create_module(term, block):
    module = Module(name=term.data)
    return module


@extend(Module)
class ExtendModule:
    render = MemFun(render_module)
