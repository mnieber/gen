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
        }
    )
