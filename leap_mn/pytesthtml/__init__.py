from leap_mn.layerconfig import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.tool import Tool
from moonleap import tags


def get_layer_config(pytest_html):
    result = dict(html_report=r"${/SERVER/install_dir}/report.html")
    return result


class PytestHtml(Tool):
    def __init__(self):
        super().__init__()


@tags(["pytest-html"])
def create_pytest_html(term, block):
    pytest_html = PytestHtml()
    pytest_html.add_to_pip_dependencies(PipDependency(["pytest-html"]))
    pytest_html.layer_config = LayerConfig(
        lambda: dict(PYTEST=get_layer_config(pytest_html))
    )
    return pytest_html
