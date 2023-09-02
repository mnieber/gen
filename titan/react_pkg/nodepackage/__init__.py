from pathlib import Path

from moonleap import create, create_forward, rule
from moonleap.blocks.verbs import has, runs

from .resources import NodePackage  # noqa


@create("node-package")
def create_node_package(term):
    node_package = NodePackage()
    return node_package


@rule("react-app", has, "node-package")
def react_app_has_node_package(react_app, node_package):
    react_app.renders(
        [node_package],
        "",
        lambda node_package: dict(node_package=node_package),
        [Path(__file__).parent / "templates"],
    )
    return create_forward(react_app.service, runs, ":node")


@rule("react-app", has, "cypress")
def react_app_has_cypress(react_app, cypress):
    react_app.set_flags(["app/useCypress"])
    return create_forward(react_app.service, runs, cypress)
