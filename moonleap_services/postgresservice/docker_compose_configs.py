from moonleap_project.dockercompose import DockerComposeConfig


def get(is_dev: bool):
    def service_body():
        body = {}
        volumes = body.setdefault("volumes", [])
        if is_dev:
            volumes.append("postgres_data:/var/lib/postgresql/data")
        return body

    def global_body():
        body = {}
        volumes = body.setdefault("volumes", {})

        if is_dev:
            volumes["postgres_data"] = {}

        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: service_body(),
        get_global_body=lambda x, service_name: global_body(),
        is_dev=is_dev,
    )
