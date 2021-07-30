from moonleap_dodo.layer import LayerConfig


def get(docker_compose):
    def inner():
        project = docker_compose.project
        name = project.name_snake + "_dev"
        return {
            "DOCKER_COMPOSE": {
                "compose_project_name": name,
                "cwd": r"${/ROOT/src_dir}",
                "files": ["docker-compose.dev.yml"],
            },
            "ROOT": {
                "aliases": {
                    "up": "docker-compose up --detach",
                    "down": "docker-compose down",
                    "build": "docker-compose build",
                }
            },
        }

    return LayerConfig(lambda x: inner())
