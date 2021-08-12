from moonleap import chop0
from titan.django_pkg.djangoapp.resources import DjangoConfig

block = chop0(
    """
GRAPHQL_AUTH = {
    "REGISTER_MUTATION_FIELDS": {
        "email": "String",
    },
    "UPDATE_MUTATION_FIELDS": ["username"],
    "LOGIN_ALLOWED_FIELDS": ["email"],
    "EMAIL_TEMPLATE_ACTIVATION": "users.email.ActivationEmail",
    "EMAIL_TEMPLATE_ACTIVATION_RESEND": "users.email.ActivationEmail",
    "EMAIL_TEMPLATE_PASSWORD_RESET": "users.email.PasswordResetEmail",
}

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=7),
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
}
"""
)


def get():
    return DjangoConfig(
        {
            "auth": {
                "AUTHENTICATION_BACKENDS": ["graphql_auth.backends.GraphQLAuthBackend"],
                "blocks": [block],
            },
            "installed_apps": {
                "THIRD_PARTY_APPS": [
                    "graphql_auth",
                    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
                ],
            },
        }
    )
