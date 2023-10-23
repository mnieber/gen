def get_contexts(_):
    result = []
    for service in _.project.services:
        result.append(dict(service=service))
    return result


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": f"../{_.service.name}",
        },
    }
