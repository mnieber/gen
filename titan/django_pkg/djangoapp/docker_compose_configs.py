from titan.project_pkg.dockercompose import DockerComposeConfig


def get(is_dev: bool):
    def service_body():
        body = {}
        environment = body.setdefault("environment", [])
        postfix = "dev" if is_dev else "prod"
        environment.append(f"DJANGO_SETTINGS_MODULE=app.settings.{postfix}")
        return body

    def global_body():
        body = {}
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: service_body(),
        get_global_body=lambda x, service_name: global_body(),
        is_dev=is_dev,
    )
