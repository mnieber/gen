from moonleap.merge_into_config import merge_into_config

from .resources import DockerComposeConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return DockerComposeConfig(body=new_body)


def merge_configs(configs):
    merged = R.reduce(merge, DockerComposeConfig(body={}), configs)
    return merged.get_body()
