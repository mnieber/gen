from titan.project_pkg.dockercompose import DockerComposeConfig


def get(target: str):
    def service_body():
        body = {}
        environment = body.setdefault("environment", [])
        environment.append(f"DJANGO_SETTINGS_MODULE=app.settings.{target}")
        return body

    def global_body():
        body = {}
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: service_body(),
        get_global_body=lambda x, service_name: global_body(),
        target=target,
        is_override=False,
    )
