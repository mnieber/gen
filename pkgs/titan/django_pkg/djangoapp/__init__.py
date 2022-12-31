from pathlib import Path

from titan.project_pkg.service import Service

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, empty_rule, extend, rule
from moonleap.blocks.verbs import connects, has, runs, uses

from .resources import DjangoAdminReorder, DjangoApp

base_tags = {
    "django-app": ["tool"],
}

rules = {
    ("django-app", uses, "admin-reorder"): empty_rule(),
}


@create("django-app")
def create_django(term):
    django_app = DjangoApp(name="django-app")
    django_app.template_dir = Path(__file__).parent / "templates"
    django_app.template_context = dict(django_app=django_app)
    return django_app


@create("admin-reorder")
def create_admin_reorder(term):
    return DjangoAdminReorder()


@rule("django-app")
def created_django(django_app):
    return create_forward(django_app, has, "app:module")


@rule("django-app", connects, "postgres:service")
def django_uses_postgres_service(django_app, postgres_service):
    return create_forward(django_app.service, uses, "postgres:service")


@extend(DjangoApp)
class ExtendDjangoApp:
    admin_reorder = P.child(uses, ":admin-reorder")


@extend(Service)
class ExtendService:
    django_app = P.child(runs, ":django-app")
    postgres = P.child(uses, "postgres:14:docker-image")
