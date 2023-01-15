from pathlib import Path

from moonleap import create, get_root_resource, rule

from .resources import NodePackage  # noqa

base_tags = {"node-package": ["tool"]}


rules = {}


@create("node-package")
def create_node_package(term):
    node_package = NodePackage(name="node-package")
    node_package.template_dir = Path(__file__).parent / "templates"
    node_package.template_context = dict(node_package=node_package)
    return node_package


@rule("cypress")
def created_cypress(cypress):
    get_root_resource().set_flags(["app/useCypress"])
