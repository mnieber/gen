from dataclasses import dataclass

import moonleap.props as P
from leap_mn.layerconfig import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.service import Service
from leap_mn.tool import Tool
from moonleap import extend, tags


def get_layer_config(pytest):
    result = dict(capture=False)

    if pytest.service and pytest.service.src_dir:
        result["src_dir"] = pytest.service.src_dir.location

    return result


@dataclass
class Pytest(Tool):
    pass


@tags(["pytest"])
def create_pytest(term, block):
    pytest = Pytest()
    pytest.add_to_pip_dependencies(PipDependency(["pytest"]))
    pytest.layer_config = LayerConfig(lambda: dict(PYTEST=get_layer_config(pytest)))
    return pytest


@extend(Pytest)
class ExtendPytest:
    service = P.parent(Service, "has", "pytest")
