def get_docker_compose_options(docker_compose):
    project = docker_compose.project
    suffix = "_dev" if docker_compose.is_dev else ""
    name = (project.name if project else "<INSERT NAME>") + suffix

    return {
        "DOCKER_COMPOSE"
        + suffix.upper(): {
            "name": name,
            "cwd": r"${/PROJECT/src_dir}",
            "files": [docker_compose.name + ".yml"],
        },
        "ROOT": {"aliases": {"up": "docker-compose up --detach"}},
    }
