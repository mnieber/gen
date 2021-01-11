from pathlib import Path

import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.service import Service
from moonleap import Resource, tags


def get_layer_config(pytest_html):
    result = dict(html_report=r"${/SERVER/install_dir}/report.html")
    return result


class PytestHtml(Resource):
    def __init__(self):
        super().__init__()


@tags(["pytest-html"])
def create_pytest_html(term, block):
    pytest_html = PytestHtml()
    pytest_html.add_child(PipDependency(["pytest-html"]))
    pytest_html.add_child(
        LayerConfig(lambda x: dict(PYTEST=get_layer_config(pytest_html)))
    )
    return pytest_html


meta = {
    PytestHtml: dict(
        props={
            "service": props.parent_of_type(Service),
        }
    )
}
