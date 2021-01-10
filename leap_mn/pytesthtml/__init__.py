from pathlib import Path

import moonleap.props as props
from leap_mn.layer import LayerConfig
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
    return [
        pytest_html,
        PipDependency(["pytest-html"]),
        LayerConfig(lambda x: dict(PYTEST=get_layer_config(pytest_html))),
    ]


meta = {
    PytestHtml: dict(
        props={
            "service": props.parent_of_type(Service),
        }
    )
}
