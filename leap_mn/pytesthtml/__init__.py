from leap_mn.layer import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.tool import Tool
from moonleap import tags

from . import layer_configs as LC


class PytestHtml(Tool):
    def __init__(self):
        super().__init__()


@tags(["pytest-html"])
def create_pytest_html(term, block):
    pytest_html = PytestHtml()
    pytest_html.add_to_pip_dependencies(PipDependency(["pytest-html"]))
    pytest_html.add_to_layer_configs(
        LayerConfig(lambda: LC.get_pytest_html_options(pytest_html))
    )
    return pytest_html
