import moonleap.resource.props as P
from leapdodo.layer import LayerConfig
from leapproject.service import Service
from leaptools.pipdependency import PipDependency
from moonleap import extend, rule, tags

from . import layer_configs as LC
from . import opt_paths
from .resources import Pytest, PytestHtml


@tags(["pytest"])
def create_pytest(term, block):
    pytest = Pytest()
    pytest.pip_dependencies.add(PipDependency(["pytest"]))
    pytest.layer_configs.add(LayerConfig(lambda: LC.get_pytest_options(pytest)))

    return pytest


@tags(["pytest-html"])
def create_pytest_html(term, block):
    pytest_html = PytestHtml()
    pytest_html.pip_dependencies.add(PipDependency(["pytest-html"]))

    pytest_html.layer_configs.add(
        LayerConfig(lambda: LC.get_pytest_html_options(pytest_html))
    )

    pytest_html.opt_paths.add(opt_paths.pytest_html_opt_path)
    return pytest_html


@rule("service", ("has", "uses"), "pytest")
def service_has_pytest(service, pytest):
    service.add_tool(pytest)
    if pytest.pytest_html:
        service.add_tool(pytest.pytest_html)


@extend(Pytest)
class ExtendPytest:
    pytest_html = P.child("with", "pytest-html")
    service = P.parent(Service, "has", "pytest")
