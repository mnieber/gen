from moonleap_django.djangoapp.resources import DjangoConfig


def get():
    return DjangoConfig(
        {
            "urls": ['path(r"admin/", admin.site.urls)'],
            "urls_imports": ["from django.contrib import admin"],
        }
    )
