from moonleap_project.dockercompose import DockerComposeConfig


def get(is_dev: bool):
    def service_body():
        body = {}
        environment = body.setdefault("environment", [])
        if is_dev:
            environment.append("CHOKIDAR_USEPOLLING=true")
        return body

    def global_body():
        body = {}
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: service_body(),
        get_global_body=lambda x, service_name: global_body(),
        is_dev=is_dev,
    )
