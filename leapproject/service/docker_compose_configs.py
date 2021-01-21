from leapproject.dockercompose import DockerComposeConfig


def get(service, is_dev):
    def inner():
        body = dict(
            depends_on=[],
            image=f"{service.project.name}_{service.name}",
            ports=["80:80"],
        )

        volumes = body.setdefault("volumes", [])
        if is_dev:
            volumes.append(f"./{service.name}:/app/src")

        dockerfile = service.dockerfile_dev if is_dev else service.dockerfile
        if dockerfile:
            build = body.setdefault("build", {})
            build["context"] = f"./{service.name}"
            build["dockerfile"] = dockerfile.name

        return body

    return DockerComposeConfig(lambda x: inner(), is_dev=is_dev)
