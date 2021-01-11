import moonleap.props as props
import ramda as R
from leap_mn.dockercompose import DockerCompose, DockerComposeDev
from moonleap import Resource
from moonleap.props import Prop
from moonleap.utils import merge_into_config
from moonleap.utils.uppercase_dict_keys import uppercase_dict_keys


class DockerComposeConfig(Resource):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def __str__(self):
        return f"DockerComposeConfig name={self.name}"

    @property
    def name(self):
        return "/".join(self.get_body().keys())

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body


class DockerComposeConfigDev(DockerComposeConfig):
    def __str__(self):
        return f"DockerComposeConfigDev name={self.name}"


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return DockerComposeConfig(new_body)


def get_config(config_type):
    def prop(self):
        configs = self.children_of_type(config_type)
        merged = R.reduce(merge, config_type({}), configs)
        return merged.get_body()

    return Prop(prop, child_resource_type=config_type)


def meta():
    return {
        DockerCompose: dict(
            props={
                "config": get_config(DockerComposeConfig),
            },
        ),
        DockerComposeDev: dict(
            props={
                "config": get_config(DockerComposeConfigDev),
            },
        ),
    }
