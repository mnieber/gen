from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, extend, rule
from moonleap.blocks.verbs import has
from titan.api_pkg.apiregistry import get_api_reg
from titan.api_pkg.apiregistry.get_form_type_specs import get_form_type_specs
from titan.api_pkg.apiregistry.get_public_type_specs import get_public_type_specs
from titan.django_pkg.djangoapp import DjangoApp
from titan.types_pkg.typeregistry import get_type_reg

from .resources import ApiModule  # noqa


@create("api:module")
def create_api_module(term):
    api_module = ApiModule(name="api", kebab_name="api")
    api_module.template_dir = Path(__file__).parent / "templates"
    api_module.template_context = lambda api_module: dict(
        api_module=api_module,
        api_reg=get_api_reg(),
        type_reg=get_type_reg(),
    )
    return api_module


@rule("django-app", has, "api:module")
def add_query_render_tasks(django_app, api_module):
    api_module.renders(
        lambda: get_api_reg().queries,
        "query",
        lambda query: dict(query=query),
        [Path(__file__).parent / "templates_query"],
    )
    api_module.renders(
        lambda: [x for x in get_api_reg().queries if not x.api_spec.is_stub],
        "tests",
        lambda query: dict(query=query),
        [Path(__file__).parent / "templates_query_tests"],
    )

    api_module.renders(
        lambda: [x for x in get_api_reg().mutations if not x.api_spec.is_stub],
        "mutation",
        lambda mutation: dict(mutation=mutation),
        [Path(__file__).parent / "templates_mutation"],
    )
    api_module.renders(
        lambda: [x for x in get_api_reg().mutations if not x.api_spec.is_stub],
        "tests",
        lambda mutation: dict(mutation=mutation),
        [Path(__file__).parent / "templates_mutation_tests"],
    )

    api_module.renders(
        lambda: get_public_type_specs(
            get_api_reg(),
            include_stubs=False,
            predicate=lambda field_spec: "server" in field_spec.has_api,
        ),
        "types",
        lambda type_spec: dict(type_spec=type_spec),
        [Path(__file__).parent / "templates_type"],
    )

    api_module.renders(
        lambda: get_form_type_specs(get_api_reg()),
        "types",
        lambda form_type_spec: dict(form_type_spec=form_type_spec),
        [Path(__file__).parent / "templates_form_type"],
    )


@extend(DjangoApp)
class ExtendDjangoApp:
    api_module = P.child(has, "api:module")