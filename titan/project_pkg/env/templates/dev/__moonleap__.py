def get_helpers(_):
    class Helpers:
        django_service = None
        react_service = None
        postgres_service = None

        def __init__(self):
            for service in _.project.services:
                if service.has_django_app:
                    self.django_service = service
                if service.has_react_app:
                    self.react_service = service
                if service.has_postgres:
                    self.postgres_service = service

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "django.env.j2": {
            "include": bool(__.django_service),
        },
        "postgres.env.j2": {
            "include": bool(__.postgres_service),
        },
        "react.env.j2": {
            "include": bool(__.react_service),
        },
    }
