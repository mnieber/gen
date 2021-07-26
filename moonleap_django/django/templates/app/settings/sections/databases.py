import environ

env = environ.Env()

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "django",
        # The following settings are not used with sqlite3:
        "USER": "django",
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "localhost",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
    },
}

MIGRATION_MODULES = {}
