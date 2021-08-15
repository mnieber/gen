from moonleap import chop0
from titan.django_pkg.djangoapp.resources import DjangoConfig

block = chop0(
    """
GRAPHENE = {
    "SCHEMA": "api.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

    """
)


def get():
    return DjangoConfig(
        settings={
            "installed_apps": {
                "THIRD_PARTY_APPS": [
                    "graphene_django",
                ],
            },
            "base": {
                "blocks": [
                    block,
                ]
            },
        },
        urls=['path(r"graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)))'],
        urls_imports=["from graphene_django.views import GraphQLView"],
        cors_urls=["graphql"],
    )
