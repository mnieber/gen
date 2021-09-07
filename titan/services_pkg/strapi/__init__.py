from dataclasses import dataclass
from pathlib import Path

from moonleap import add, create, rule
from moonleap.verbs import connects, uses
from titan.project_pkg.service import Tool
from titan.tools_pkg.pipdependency import PipDependency, PipRequirement
from titan.tools_pkg.pkgdependency import PkgDependency

from . import dodo_layer_configs, makefile_rules

strapi_env_fn = "./env/strapi.env"


@dataclass
class Strapi(Tool):
    pass


@create("strapi", ["tool"])
def create_strapi(term, block):
    strapi = Strapi(name="strapi")
    add(strapi, makefile_rules.get_runserver())
    add(strapi, makefile_rules.get_debugserver())
    add(strapi, dodo_layer_configs.get())
    return strapi


@rule("service", uses, "strapi")
def service_uses_strapi(service, strapi):
    service.install_dir = "/srv/app"
    service.port = service.port or "1337"
    service.env_files.append(strapi_env_fn)
    add(service.project, dodo_layer_configs.get_for_project(service.name))


@rule("strapi", connects, "postgres:service")
def strapi_uses_postgres_service(strapi, postgres_service):
    add(strapi, PkgDependency(["postgresql-client"], is_dev=True))
    add(strapi, PipRequirement(["psycopg2"]))
    add(
        strapi,
        PipDependency(["pgcli==2.1.1"], is_dev=True),
    )
    add(
        strapi,
        PipRequirement(
            ["git+git://github.com/jnoortheen/django-pgcli@master#egg=django-pgcli"],
            is_dev=True,
        ),
    )
    add(strapi, makefile_rules.get_createdb())
    postgres_service.project.add_template_dir(
        Path(__file__).parent / "templates_project"
    )
