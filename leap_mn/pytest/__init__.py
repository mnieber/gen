import moonleap.props as props
from leap_mn.layer import LayerConfig
from leap_mn.pipdependency import PipDependency
from leap_mn.service import Service
from moonleap import Resource, tags
from moonleap.config import derive


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
    return [
        pytest,
        PipDependency(["pytest"]),
        LayerConfig("pytest", lambda x: get_layer_config(pytest)),
    ]


meta = {
    Pytest: dict(
        props={
            "service": props.parent_of_type(Service),
        }
    )
}
