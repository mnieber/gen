from leap_mn.pipdependency import PipDependency
from moonleap import Always, Resource
from moonleap.config import reduce


class PytestHtml(Resource):
    def __init__(self):
        pass


def create(term, block):
    return [PytestHtml(), PipDependency("pytest-html")]


@reduce(a_resource="leap_mn.Pytest", b_resource=PytestHtml)
def add_pytest_html(pytest, pytest_html):
    if pytest.is_created_in_block_that_mentions(pytest):
        pytest.pytest_html = pytest_html


tags = ["pytest-html"]
