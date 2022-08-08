from titan.project_pkg.dockercompose import DockerComposeConfig


def get(target: str):
    def service_body():
        body = {}
        if target == "dev":
            environment = body.setdefault("environment", [])
            environment.append("CHOKIDAR_USEPOLLING=true")
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
