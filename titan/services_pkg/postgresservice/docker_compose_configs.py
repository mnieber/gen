from titan.project_pkg.dockercompose import DockerComposeConfig


def get(target: str):
    def service_body():
        body = {}
        volumes = body.setdefault("volumes", [])
        if target == "dev":
            volumes.append("postgres_data:/var/lib/postgresql/data")
        return body

    def global_body():
        body = {}
        volumes = body.setdefault("volumes", {})

        if target == "dev":
            volumes["postgres_data"] = {}

        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: service_body(),
        get_global_body=lambda x, service_name: global_body(),
        target=target,
        is_override=False,
    )
