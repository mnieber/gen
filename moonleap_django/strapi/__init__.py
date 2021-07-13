from dataclasses import dataclass

import moonleap.resource.props as P
from moonleap import add, extend, rule, tags
from moonleap.verbs import connects, uses
from moonleap_project.service import Service
from moonleap_tools.pipdependency import PipDependency, PipRequirement
from moonleap_tools.pkgdependency import PkgDependency
from moonleap_tools.tool import Tool

from . import layer_configs, makefile_rules

strapi_env_fn = "./env/strapi.env"


@dataclass
class Strapi(Tool):
    pass


@tags(["strapi"])
def create_strapi(term, block):
    strapi = Strapi(name="strapi")
    add(strapi, makefile_rules.get())
    add(strapi, layer_configs.get())
    return strapi


@rule("service", uses, "strapi")
def service_uses_strapi(service, strapi):
    service.install_dir = "/srv/app"
    service.port = service.port or "1337"
    service.env_files.append(strapi_env_fn)
    add(service.project, layer_configs.get_for_project(service.name))


@rule("strapi", connects, "postgres:service")
def strapi_uses_postgres_service(strapi, postgres_service):
    add(strapi, PkgDependency(["postgresql-client", "psycopg2-binary"], is_dev=True))
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
    add(strapi, makefile_rules.get_postgres())
    postgres_service.project.add_template_dir(__file__, "templates_project")
