def get_helpers(_):
    class Helpers:
        modules = [
            module for module in _.django_app.modules if module.has_graphql_schema
        ]

    return Helpers()
