import typing as T
from dataclasses import dataclass

import moonleap.props as props
import ramda as R
from leap_mn.dockercompose import DockerCompose
from moonleap import Resource
from moonleap.config import extend
from moonleap.merge_into_config import merge_into_config


@dataclass
class DockerComposeConfig(Resource):
    body: T.Union[dict, T.Callable]

    def __repr__(self):
        return f"DockerComposeConfig name={self.name}"

    @property
    def name(self):
        return "/".join(self.get_body().keys())

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return DockerComposeConfig(body=new_body)


def merge_configs(configs):
    merged = R.reduce(merge, DockerComposeConfig(body={}), configs)
    return merged.get_body()


def meta():
    @extend(DockerCompose)
    class ExtendDockerCompose:
        config = props.children("has", "docker-compose-config", rdcr=merge_configs)
        configs = props.children("has", "docker-compose-config")

    return [ExtendDockerCompose]
