from moonleap_project.dockercompose import DockerComposeConfig


def get(service, is_dev):
    def inner():
        body = dict(
            depends_on=[],
            image=f"{service.project.name}_{service.name}",
            ports=[f"{service.port}:{service.port}"],
        )

        volumes = body.setdefault("volumes", [])
        if is_dev:
            volumes.append(f"./{service.name}:/app/src")

        dockerfile = service.dockerfile_dev if is_dev else service.dockerfile
        if dockerfile:
            build = body.setdefault("build", {})
            build["context"] = f"./{service.name}"
            build["dockerfile"] = dockerfile.name

        if is_dev:
            body["command"] = "sleep infinity"

        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: inner(),
        get_global_body=lambda x, service_name: {},
        is_dev=is_dev,
    )
