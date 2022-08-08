import ramda as R
from moonleap import get_session
from moonleap.utils.merge_into_config import merge_into_config


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs)
    merge_into_config(new_body, rhs)
    return new_body


def get_docker_compose_config(self, target, is_override):
    config = {}
    services = config.setdefault("services", {})
    for service in self.services:
        docker_compose_configs = R.pipe(
            R.always(service.docker_compose_configs.merged),
            R.filter(lambda x: x.target == target and x.is_override == is_override),
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


def get_docker_compose_override_fn(self):
    return get_session().get_tweak_or(
        "docker-compose.dev.override.yml", ["docker_compose_override_fn"]
    )
