def get_helpers(_):
    class Helpers:
        dockerfile = _.service.dockerfile
        docker_image = dockerfile.docker_image if dockerfile else None

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "include": bool(_.project.docker_compose and _.service.dockerfile),
            "name": "..",
        },
        "Dockerfile.prod.j2": {
            "include": bool(_.project.has_prod_config),
        },
    }

