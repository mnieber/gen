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
