from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, extend, rule
from moonleap.verbs import has, runs, uses
from titan.project_pkg.service import Service, Tool

from .resources import Vandelay

base_tags = {
    "black": ["tool"],
    "cypress": ["tool"],
    "fish": ["tool"],
    "isort": ["tool"],
    "opt-dir": ["tool"],
    "pip-compile": ["tool"],
    "prettier": ["tool"],
    "pudb": ["tool"],
    "pytest": ["tool"],
    "setup.cfg": ["tool"],
    "tailwind-css": ["tool"],
    "uikit": ["tool"],
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


@rule("cypress")
def created_cypress(cypress):
    return create_forward(":node-package", has, "cypress:node-pkg")


@rule("uikit")
def created_uikit(uikit):
    return create_forward(":node-package", has, "uikit:node-pkg")


@rule("tailwind-css")
def created_tailwind_css(tailwind_css):
    return create_forward(":node-package", has, "tailwind-css:node-pkg")


@rule("setup.cfg")
def created_setupcfg(setupcfg):
    setupcfg.template_dir = Path(__file__).parent / "templates_setupcfg"


@rule("pip-compile")
def created_pip_compile(pip_compile):
    pip_compile.template_dir = Path(__file__).parent / "templates_pip_compile"


@rule("service", runs + uses, "vandelay")
def service_uses_vandelay(service, vandelay):
    if vandelay.language == "js":
        template_dir = "templates_vandelay_js"
    elif vandelay.language == "py":
        template_dir = "templates_vandelay_py"
    else:
        raise Exception("Unknown language", vandelay.language)

    service.project.renders(
        [vandelay],
        ".vandelay",
        dict(service=service),
        [Path(__file__).parent / template_dir],
    )


@extend(Service)
class ExtendService:
    black = P.child(runs + uses, "black")
    cypress = P.child(runs + uses, "cypress")
    fish = P.child(runs + uses, "fish")
    isort = P.child(runs + uses, "isort")
    opt_dir = P.child(runs + uses, "opt-dir")
    pip_compile = P.child(runs + uses, "pip-compile")
    prettier = P.child(runs + uses, "prettier")
    pudb = P.child(runs + uses, "pudb")
    pytest = P.child(runs + uses, "pytest")
    setup_cfg = P.child(runs + uses, "setup.cfg")
    tailwindcss = P.child(runs + uses, "tailwind-css")
    uikit = P.child(runs + uses, "uikit")
    vandelay = P.child(runs + uses, "vandelay")
