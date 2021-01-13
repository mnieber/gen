def get_service_options(service, docker_compose_config):
    is_dev = docker_compose_config.is_dev
    volumes = dict(volumes=[f"./{service.name}:/app/src"])

    body = dict(
        depends_on=[],
        image=f"{service.project.name}_{service.name}",
        ports=["80:80"],
        **(volumes if is_dev else {}),
    )

    dockerfile = service.dockerfile_dev if is_dev else service.dockerfile

    if dockerfile:
        body["build"] = dict(
            context=f"./{service.name}",
            dockerfile=dockerfile.name,
        )

    return {service.name: body}
