def get_helpers(_):
    class Helpers:
        dockerfile = _.service.dockerfile
        docker_image = dockerfile.docker_image

    return Helpers()
