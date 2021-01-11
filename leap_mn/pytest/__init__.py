import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.service import Service
from moonleap import Resource, tags


def get_layer_config(pytest):
    result = dict(capture=False)

    if pytest.service and pytest.service.src_dir:
        result["src_dir"] = pytest.service.src_dir.location

    return result


class Pytest(Resource):
    def __init__(self):
        super().__init__()


@tags(["pytest"])
def create_pytest(term, block):
    pytest = Pytest()
    pytest.add_child(PipDependency(["pytest"]))
    pytest.add_child(LayerConfig(lambda x: dict(PYTEST=get_layer_config(pytest))))
    return pytest


meta = {
    Pytest: dict(
        props={
            "service": props.parent_of_type(Service),
        }
    )
}
