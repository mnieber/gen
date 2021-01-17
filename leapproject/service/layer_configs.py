def get_service_options():
    return dict(
        #
        SERVER=dict(
            #
            install_dir="/app",
            src_dir="${/SERVER/install_dir}/src",
        )
    )


def get_docker_options(service):
    project = service.project

    return dict(
        #
        DOCKER_OPTIONS={
            #
            "*": {"container": f"{project.name}_{service.name}_1"}
        }
    )
