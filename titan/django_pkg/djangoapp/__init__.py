from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, extend, rule
from moonleap.verbs import connects, has, runs, uses
from titan.project_pkg.service import Service

from .resources import DjangoApp

base_tags = [
    ("django-app", ["tool"]),
]


@create("django-app")
def create_django(term):
    django_app = DjangoApp(name="django-app")
    django_app.template_dir = Path(__file__).parent / "templates"
    django_app.template_context = dict(django_app=django_app)
    return django_app


@rule("django-app")
def created_django(django_app):
    return create_forward(django_app, has, "app:module")


@rule("django-app", connects, "postgres:service")
def django_uses_postgres_service(django_app, postgres_service):
    return create_forward(django_app.service, uses, "postgres:service")


@extend(Service)
class ExtendService:
    django_app = P.child(runs, ":django-app")
    postgres = P.child(uses, "postgres:14:docker-image")
