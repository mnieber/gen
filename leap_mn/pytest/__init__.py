from leap_mn.layer import LayerConfig
from leap_mn.pipdependency import PipDependency
from moonleap import Resource
from moonleap.config import derive


def get_layer_config():
    return {"PYTEST": {"pytesthtml": False}}


class Pytest(Resource):
    def __init__(self):
        super().__init__()
        self.pytest_html = None

    def describe(self):
        return dict(
            pytest_html=self.pytest_html.describe() if self.pytest_html else None
        )


def create(term, block):
    return [Pytest(), PipDependency("pytest")]


@derive(resource=Pytest)
def create_layer_config(pytest):
    return [LayerConfig("pytest", get_layer_config())]


tags = ["pytest"]
