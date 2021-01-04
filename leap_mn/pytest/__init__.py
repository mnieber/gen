from leap_mn.layer import LayerConfig
from leap_mn.pipdependency import PipDependency
from moonleap import Resource, tags
from moonleap.config import derive


def get_layer_config():
    return {"PYTEST": {"pytesthtml": False}}


class Pytest(Resource):
    def __init__(self):
        super().__init__()
        self.pytest_html = None


@tags(["pytest"])
def create(term, block):
    return [Pytest(), PipDependency("pytest")]


@derive(Pytest)
def create_layer_config(pytest):
    return [LayerConfig("pytest", get_layer_config())]
