from dataclasses import dataclass

import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.service import Service
from leap_mn.tool import Tool
from moonleap import extend, tags

from . import layer_configs as LC


@dataclass
class Pytest(Tool):
    pass


@tags(["pytest"])
def create_pytest(term, block):
    pytest = Pytest()
    pytest.add_to_pip_dependencies(PipDependency(["pytest"]))
    pytest.add_to_layer_configs(
        #
        LayerConfig(lambda: LC.get_pytest_options(pytest))
    )
    return pytest


@extend(Pytest)
class ExtendPytest:
    service = P.parent(Service, "has", "pytest")
