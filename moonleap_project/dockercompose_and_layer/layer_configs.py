from moonleap_dodo.layer import LayerConfig


def get(docker_compose):
    def inner():
        project = docker_compose.project
        suffix = "_dev" if docker_compose.is_dev else ""
        name = (project.name if project else "<INSERT NAME>") + suffix
        return {
            "DOCKER_COMPOSE"
            + suffix.upper(): {
                "name": name,
                "cwd": r"${/ROOT/src_dir}",
                "files": [docker_compose.name + ".yml"],
            },
            "ROOT": {
                "aliases": {
                    "up": "docker-compose --dev up --detach",
                    "down": "docker-compose --dev down",
                    "build": "docker-compose --dev build",
                }
            },
        }

    return LayerConfig(lambda x: inner())
