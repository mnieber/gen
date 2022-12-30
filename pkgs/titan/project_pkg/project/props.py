def get_service_by_name(project, service_name, default="__notset__"):
    for x in project.services:
        if x.name == service_name:
            return x

    if default == "__notset__":
        raise KeyError(f"No service named {service_name}")

    return default
