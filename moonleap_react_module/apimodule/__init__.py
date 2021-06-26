from moonleap import add, rule
from moonleap_react.nodepackage import load_node_package_config


@rule("api:module")
def api_module_created(api_module):
    add(api_module, load_node_package_config(__file__))
