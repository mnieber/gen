from moonleap_project.dockercompose import DockerComposeConfig


def get(service, is_dev):
    def inner():
        image_postfix = "_dev" if is_dev else ""

        port = service.port or "80"
        body = dict(
            depends_on=[],
            ports=[f"{port}:{port}"],
            image=(
                f"{service.project.name}_{service.name}{image_postfix}"
                if service.dockerfile
                else service.docker_image.name
            ),
        )

        if service.env_files:
            env_file_section = body.setdefault("env_file", [])
            for env_file in service.env_files:
                if env_file not in env_file_section:
                    env_file_section.append(env_file)

        if is_dev and service.env_files_dev:
            env_file_section = body.setdefault("env_file", [])
            for env_file in service.env_files_dev:
                if env_file not in env_file_section:
                    env_file_section.append(env_file)

        volumes = body.setdefault("volumes", [])
        if is_dev and service.dockerfile:
            volumes.append(f"./{service.name}:{service.install_dir}/src")
            body["command"] = "sleep infinity"

        if service.dockerfile:
            build = body.setdefault("build", {})
            build["context"] = f"./{service.name}"
            build["dockerfile"] = "Dockerfile" + (".dev" if is_dev else ".prod")

        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: inner(),
        get_global_body=lambda x, service_name: {},
        is_dev=is_dev,
    )


def add_depends_on(depends_on_service, is_dev):
    def inner():
        body = {}
        depends_on = body.setdefault("depends_on", [])
        depends_on.append(depends_on_service.name)
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: inner(),
        get_global_body=lambda x, service_name: {},
        is_dev=is_dev,
    )
