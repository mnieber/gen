from leap_mn.layer import LayerConfig
from leap_mn.pipdependency import PipDependency
from moonleap import Always, Resource
from moonleap.config import reduce


def get_layer_config():
    return {"PYTEST": {"pytesthtml": False}}


class Pytest(Resource):
    def __init__(self):
        self.pytest_html = None

    def describe(self):
        return dict(pytest_html=self.pytest_html.describe())


def create(term, block):
    return [Pytest(), PipDependency("pytest")]


@reduce(parent_resource=Always, resource=Pytest, delay=True)
def create_layer_config(always, pytest):
    return [LayerConfig("pytest", get_layer_config())]


tags = ["pytest"]
