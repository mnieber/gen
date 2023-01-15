import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend, kebab_to_camel
from moonleap.blocks.verbs import has
from titan.project_pkg.project import Project

from .resources import Config

rules = {
    ("project", has, "config"): empty_rule(),
}


@create("config")
def create_config(term):
    return Config(name=kebab_to_camel(term.data))


@extend(Project)
class ExtendProject:
    has_dev_config = P.child(has, "dev:config")
    has_prod_config = P.child(has, "prod:config")
