import moonleap.extension.props as P
from moonleap import create, extend
from moonleap.spec.verbs import runs, uses
from titan.project_pkg.service import Service, Tool

from .resources import Vandelay

base_tags = {
    "black": ["tool"],
    "cypress": ["tool"],
    "fish": ["tool"],
    "isort": ["tool"],
    "opt-dir": ["tool"],
    "node": ["tool"],
    "pip-compile": ["tool"],
    "prettier": ["tool"],
    "pudb": ["tool"],
    "pytest": ["tool"],
    "setup.cfg": ["tool"],
    "vandelay": ["tool"],
}


@create("tool")
def create_tool(term):
    name = term.tag
    tool = Tool(name=name)
    return tool


@create("vandelay")
def create_vandelay(term):
    return Vandelay(name=term.tag, language=term.data)


@extend(Service)
class ExtendService:
    black = P.child(runs + uses, "black")
    cypress = P.child(runs + uses, "cypress")
    fish = P.child(runs + uses, "fish")
    isort = P.child(runs + uses, "isort")
    node = P.child(runs + uses, "node")
    opt_dir = P.child(runs + uses, "opt-dir")
    pip_compile = P.child(runs + uses, "pip-compile")
    prettier = P.child(runs + uses, "prettier")
    pudb = P.child(runs + uses, "pudb")
    pytest = P.child(runs + uses, "pytest")
    setup_cfg = P.child(runs + uses, "setup.cfg")
    vandelay = P.child(runs + uses, "vandelay")
