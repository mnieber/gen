import moonleap.resource.props as P
from moonleap import add, create, create_forward, empty_rule, extend, rule
from moonleap.verbs import has, with_
from titan.tools_pkg.pipdependency import PipRequirement

from . import dodo_layer_configs, opt_paths
from .resources import Pytest, PytestHtml

base_tags = [("pytest", ["tool"]), ("pytest-html", ["tool"])]


@create("pytest")
def create_pytest(term, block):
    pytest = Pytest(name="pytest")

    add(pytest, PipRequirement(["pytest"], is_dev=True))
    add(pytest, dodo_layer_configs.get_pytest_options(pytest))

    return pytest


@create("pytest-html")
def create_pytest_html(term, block):
    pytest_html = PytestHtml(name="pytest-html")

    add(pytest_html, PipRequirement(["pytest-html"], is_dev=True))
    add(pytest_html, dodo_layer_configs.get_pytest_html_options(pytest_html))
    add(pytest_html, opt_paths.pytest_html_opt_path)
    add(pytest_html, opt_paths.pytest_html_asset_path)

    return pytest_html


@rule("service", has, "pytest")
def service_has_pytest_html(service, pytest):
    if pytest.pytest_html:
        return create_forward(service, has, pytest.pytest_html)


rules = [(("pytest", with_, "pytest-html"), empty_rule())]


@extend(Pytest)
class ExtendPytest:
    pytest_html = P.child(with_, "pytest-html")
