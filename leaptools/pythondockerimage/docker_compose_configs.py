from leapproject.dockercompose import DockerComposeConfig


def get(docker_image):
    def get_service_body(service_name):
        body = {}
        volumes = body.setdefault("volumes", [])
        volumes.append(
            dict(
                type="volume",
                source=f"{service_name}_site_packages",
                target="/usr/local/lib/python3.9/site-packages",
            )
        )
        return body

    def get_global_body(service_name):
        body = {}
        volumes = body.setdefault("volumes", {})
        volumes[f"{service_name}_site_packages"] = {}
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: get_service_body(service_name),
        get_global_body=lambda x, service_name: get_global_body(service_name),
        is_dev=True,
    )
