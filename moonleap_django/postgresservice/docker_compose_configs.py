from moonleap_project.dockercompose import DockerComposeConfig


def get(is_dev: bool):
    def service_body():
        body = {}

        volumes = body.setdefault("volumes", [])
        volumes.append("postgres_data:/var/lib/postgresql/data")

        ports = body.setdefault("ports", [])
        ports.append("5432:5432")

        env_file = body.setdefault("env_file", [])
        env_file.append("./env/postgres.env")

        body["image"] = "postgres:11.5"
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
