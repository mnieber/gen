from titan.django_pkg.djangoapp.resources import DjangoConfig


def get():
    return DjangoConfig(
        settings={
            "installed_apps": {
                "THIRD_PARTY_APPS": [
                    "graphene_django",
                ],
            },
            "base": {
                "GRAPHENE": {
                    "SCHEMA": "api.schema.schema",
                }
            },
        },
        urls=['path(r"graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)))'],
        urls_imports=["from graphene_django.views import GraphQLView"],
        cors_urls=["graphql"],
    )
