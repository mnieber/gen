import moonleap.resource.props as P
from moonleap_project.service import Service
from moonleap_tools.pipdependency import PipDependency
from moonleap import add, extend, rule, tags
from moonleap.verbs import has, with_

from . import layer_configs, opt_paths
from .resources import Pytest, PytestHtml


@tags(["pytest"])
def create_pytest(term, block):
    pytest = Pytest()

    add(pytest, PipDependency(["pytest"]))
    add(pytest, layer_configs.get_pytest_options(pytest))

    return pytest


@tags(["pytest-html"])
def create_pytest_html(term, block):
    pytest_html = PytestHtml()

    add(pytest_html, PipDependency(["pytest-html"]))
    add(pytest_html, layer_configs.get_pytest_html_options(pytest_html))
    add(pytest_html, opt_paths.pytest_html_opt_path)
    add(pytest_html, opt_paths.pytest_html_asset_path)

    return pytest_html


@rule("service", has, "pytest")
def service_has_pytest(service, pytest):
    service.add_tool(pytest)
    if pytest.pytest_html:
        service.add_tool(pytest.pytest_html)


@extend(Pytest)
class ExtendPytest:
    pytest_html = P.child(with_, "pytest-html")
    service = P.parent(Service, has, "pytest")
