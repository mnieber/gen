from titan.project_pkg.dockercompose import DockerComposeConfig


def get(docker_image):
    def get_service_body(service_name):
        body = {}
        volumes = body.setdefault("volumes", [])
        volumes.extend(
            [
                f"{service_name}_venv:/app/env",
            ]
        )
        return body

    def get_global_body(service_name):
        body = {}
        volumes = body.setdefault("volumes", {})
        volumes[f"{service_name}_venv"] = {}
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: get_service_body(service_name),
        get_global_body=lambda x, service_name: get_global_body(service_name),
        target="dev",
        is_override=False,
    )
