from leapdodo.layer import LayerConfig


def get_service_options():
    def inner():
        return dict(
            #
            SERVER=dict(
                #
                install_dir="/app",
                src_dir="${/SERVER/install_dir}/src",
            )
        )

    return LayerConfig(body=lambda x: inner())


def get_docker_options(service):
    def inner():
        project = service.project

        return dict(
            #
            DOCKER_OPTIONS={
                #
                "*": {"container": f"{project.name}_{service.name}_1"}
            }
        )

    return LayerConfig(body=lambda x: inner())
