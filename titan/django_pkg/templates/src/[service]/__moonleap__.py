def get_contexts(_):
    return [dict(service=service) for service in _.project.services if service.has_django_app]

    
def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": f"../{_.service.name}",
        }
    }

