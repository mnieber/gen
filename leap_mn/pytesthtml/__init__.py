from leap_mn.layerconfig import LayerConfig
from moonleap import Always, Resource
from moonleap.config import reduce


class PytestHtml(Resource):
    def __init__(self):
        pass


def create(term, block):
    return [PytestHtml()]


@reduce(parent_resource="leap_mn.Pytest", resource=PytestHtml)
def add_pytest_html(pytest, pytest_html):
    if pytest.is_created_in_block_that_mentions(pytest):
        pytest.pytest_html = pytest_html


tags = ["pytest-html"]
