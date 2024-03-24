from moonleap import create, create_forward
from moonleap.spec.verbs import has, runs

from .resources import NodePackage  # noqa


@create("node-package")
def create_node_package(term):
    node_package = NodePackage()
    return node_package


def react_app_has_cypress(react_app, cypress):
    react_app.set_flags(["app/useCypress"])
    return create_forward(react_app.service, runs, cypress)


rules = {
    "react-app": {
        (has, "cypress"): (
            # then the service runs cypress
            react_app_has_cypress
        ),
        (has, "node-package"): (
            #
            lambda react_app, node_package: create_forward(
                react_app.service, runs, ":node"
            )
        ),
    }
}
