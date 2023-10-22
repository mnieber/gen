def get_contexts(_):
    result = []
    for service in _.project.services:
        result.append(dict(service=service))
