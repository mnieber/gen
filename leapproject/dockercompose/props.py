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
        services[service.name] = R.pipe(
            R.always(service.docker_compose_configs.merged),
            R.filter(lambda x: x.is_dev == self.is_dev),
            R.reduce(merge, DockerComposeConfig(body={})),
            lambda x: x.get_body(),
        )(None)
    return config
