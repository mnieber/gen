from moonleap.utils.case import sn
from titan.dodo_pkg.layer import LayerConfig


def get_service_options(service):
    def inner():
        return dict(
            SERVER=dict(
                #
                install_dir=service.install_dir,
                src_dir="${/SERVER/install_dir}/src",
            ),
            ROOT=dict(
                decorators=dict(docker=["exec"]),
                aliases=dict(shell=f"exec {service.shell}"),
            ),
        )

    return LayerConfig(body=lambda x: inner())


def get_docker_options(service):
    def inner():
        project = service.project

        return dict(
            #
            DOCKER_OPTIONS={
                #
                "*": {"container": f"{sn(project.kebab_name)}-dev_{service.name}_1"}
            }
        )

    return LayerConfig(body=lambda x: inner())
