from pathlib import Path


def _make_abs(service, p):
    base_path = Path("/opt") / service.project.name / service.name
    result = Path(p)
    if not result.is_absolute():
        result = base_path / p
    return result


def get_service_options(service, docker_compose_config):
    is_dev = docker_compose_config.is_dev

    body = dict(
        depends_on=[],
        image=f"{service.project.name}_{service.name}",
        ports=["80:80"],
    )

    volumes = body.setdefault("volumes", [])
    if is_dev:
        volumes.append(f"./{service.name}:/app/src")

    dockerfile = service.dockerfile_dev if is_dev else service.dockerfile
    build = body.setdefault("build", {})
    if dockerfile:
        build["context"] = f"./{service.name}"
        build["dockerfile"] = dockerfile.name

    opt_dir = service.opt_dir
    if opt_dir and is_dev:
        for tool in service.tools:
            for opt_path in tool.opt_paths.merged:
                from_path = _make_abs(service, opt_path.from_path)
                to_path = _make_abs(service, opt_path.to_path)
                volumes.append(f"{str(from_path)}:{str(to_path)}")

    return {service.name: body}
