def get_layer_config(docker_compose):
    project = docker_compose.project
    suffix = "_dev" if docker_compose.is_dev else ""
    name = (project.name if project else "<INSERT NAME>") + suffix
    return {"DOCKER_COMPOSE" + suffix.upper(): {"name": name}}
