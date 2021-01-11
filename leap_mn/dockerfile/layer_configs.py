def get_layer_config(service):
    project = service.project

    return dict(
        #
        DOCKER_OPTIONS={
            #
            "*": {"container": f"{project.name}_{service.name}_1"}
        }
    )
