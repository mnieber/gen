import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.optpath import OptPath
from leap_mn.pipdependency import PipDependency
from leap_mn.service import Service
from leap_mn.tool import Tool
from moonleap import extend, rule, tags

from . import layer_configs as LC
from .resources import Pytest, PytestHtml


@tags(["pytest"])
def create_pytest(term, block):
    pytest = Pytest()
    pytest.add_to_pip_dependencies(PipDependency(["pytest"]))
    pytest.layer_configs.add(LayerConfig(lambda: LC.get_pytest_options(pytest)))

    pytest.opt_paths.add(
        OptPath(
            is_dir=False,
            from_path="/opt/prname/foo.html",
            to_path="/opt/prname/foo.html",
        )
    )

    return pytest


@tags(["pytest-html"])
def create_pytest_html(term, block):
    pytest_html = PytestHtml()
    pytest_html.add_to_pip_dependencies(PipDependency(["pytest-html"]))

    pytest_html.layer_configs.add(
        LayerConfig(lambda: LC.get_pytest_html_options(pytest_html))
    )

    pytest_html.opt_paths.add(
        OptPath(
            is_dir=False,
            from_path="/opt/prname/pytest_report.html",
            to_path="/opt/prname/pytest_report.html",
        )
    )
    return pytest_html


@rule("pytest", "with", "pytest-html")
def pytest_with_pytest_html(pytest, pytest_html):
    pytest.layer_configs.add_source(pytest_html)
    pytest.opt_paths.add_source(pytest_html)


@extend(Pytest)
class ExtendPytest:
    service = P.parent(Service, "has", "pytest")
