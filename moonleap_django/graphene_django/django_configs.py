from moonleap import chop0
from moonleap_django.djangoapp.resources import DjangoConfig

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
        {
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
            "urls": [
                'path(r"graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)))'
            ],
            "urls_imports": [
                "from graphene_django.views import GraphQLView",
                "from django.views.decorators.csrf import csrf_exempt",
            ],
        }
    )
