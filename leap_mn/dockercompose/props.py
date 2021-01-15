import ramda as R
from moonleap.utils.merge_into_config import merge_into_config

from .resources import DockerComposeConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return DockerComposeConfig(body=new_body)


def get_docker_compose_config(self, is_dev=False):
    fltr = R.filter(lambda x: x.is_dev == is_dev)
    return R.reduce(
        merge, DockerComposeConfig(body={}), fltr(self.docker_compose_configs.merged)
    )
