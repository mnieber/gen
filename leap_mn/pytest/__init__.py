import moonleap.props as props
from leap_mn.layer import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.pytesthtml import PytestHtml
from moonleap import Resource, tags
from moonleap.config import derive


def get_layer_config():
    return {"pytesthtml": False}


class Pytest(Resource):
    def __init__(self):
        super().__init__()


@tags(["pytest"])
def create_pytest(term, block):
    return [Pytest(), PipDependency(["pytest"])]


@derive(Pytest)
def create_layer_config(pytest):
    return [LayerConfig("pytest", get_layer_config())]


meta = {Pytest: dict(props={"pytest_html": props.child_of_type(PytestHtml)})}
