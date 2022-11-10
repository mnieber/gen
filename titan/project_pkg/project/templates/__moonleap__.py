def get_helpers(_):
    class Helpers:
        has_python = [
            service
            for service in _.project.services
            if service.docker_image and service.docker_image.name.startswith("python")
        ]

    return Helpers()
