from moonleap import add, tags
from moonleap_react.module import create_module
from moonleap_react.nodepackage import load_node_package_config


@tags(["forms:module"])
def create_forms_module(term, block):
    module = create_module(term, block)
    module.add_template_dir(__file__, "templates")
    add(module, load_node_package_config(__file__))
    return module
