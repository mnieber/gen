def get_service_options(service, is_dev):
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

    return body
