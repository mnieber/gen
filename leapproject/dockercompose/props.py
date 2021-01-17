import ramda as R
from moonleap.utils.merge_into_config import merge_into_config

from .resources import DockerComposeConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return DockerComposeConfig(body=new_body)


def get_docker_compose_config(self):
    config = {}
    services = config.setdefault("services", {})
    for service in self.services:
        fltr = R.filter(lambda x: x.is_dev == self.is_dev)
        service_configs = fltr(service.docker_compose_configs.merged)
        merged_service_config = R.reduce(
            merge, DockerComposeConfig(body={}), service_configs
        )
        services[service.name] = merged_service_config.get_body()
    return config
