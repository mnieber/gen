import ramda as R
from moonleap.utils.merge_into_config import merge_into_config


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs)
    merge_into_config(new_body, rhs)
    return new_body


def get_docker_compose_config(self):
    config = {}
    services = config.setdefault("services", {})
    for service in self.services:
        docker_compose_configs = R.pipe(
            R.always(service.docker_compose_configs.merged),
            R.filter(lambda x: x.is_dev == self.is_dev),
        )(None)

        service_body = R.pipe(
            R.always(docker_compose_configs),
            R.map(lambda x: x.get_service_body(x, service.name)),
            R.reduce(merge, {}),
        )(None)

        global_body = R.pipe(
            R.always(docker_compose_configs),
            R.map(lambda x: x.get_global_body(x, service.name)),
            R.reduce(merge, {}),
        )(None)

        merge_into_config(services.setdefault(service.name, {}), service_body)
        merge_into_config(config, global_body)

    return config
