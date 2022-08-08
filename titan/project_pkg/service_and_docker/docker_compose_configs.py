from moonleap.utils.case import sn
from titan.project_pkg.dockercompose import DockerComposeConfig


def get(service, target):
    def inner():
        if not service.dockerfile and not service.docker_image:
            return {}

        image_postfix = "-dev" if target == "dev" else ""

        port = service.port or "80"
        body = dict(
            depends_on=[],
            ports=[f"{port}:{port}"],
            image=(
                f"{sn(service.project.kebab_name)}-{service.name}{image_postfix}"
                if service.dockerfile
                else service.docker_image.name
            ),
        )

        if service.env_files:
            env_file_section = body.setdefault("env_file", [])
            for env_file in service.env_files:
                if env_file not in env_file_section:
                    env_file_section.append(env_file)

        if target == "dev" and service.env_files_dev:
            env_file_section = body.setdefault("env_file", [])
            for env_file in service.env_files_dev:
                if env_file not in env_file_section:
                    env_file_section.append(env_file)

        volumes = body.setdefault("volumes", [])
        if target == "dev" and service.dockerfile:
            volumes.append(f"./{service.name}:{service.install_dir}/src")
            body["command"] = "sleep infinity"

        if service.dockerfile:
            build = body.setdefault("build", {})
            build["context"] = f"./{service.name}"
            build["dockerfile"] = "Dockerfile" + "." + target

        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: inner(),
        get_global_body=lambda x, service_name: {},
        target=target,
        is_override=False,
    )


def add_depends_on(depends_on_service, target):
    def inner():
        body = {}
        depends_on = body.setdefault("depends_on", [])
        depends_on.append(depends_on_service.name)
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: inner(),
        get_global_body=lambda x, service_name: {},
        target=target,
        is_override=False,
    )
