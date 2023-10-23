def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": "..",
        }
    }


def get_contexts(_):
    return [
        dict(service=service)
        for service in _.project.services
        if service.vandelay and service.vandelay.language == "py"
    ]
