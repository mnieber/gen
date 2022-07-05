import moonleap.resource.props as P
from moonleap import add, create_forward, extend, feeds, rule
from moonleap.verbs import has, uses
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.project import Project

from . import dodo_layer_configs

rules = [(("project", has, "config:layer"), feeds("dodo_layer_configs"))]


@rule("project", has, "config:layer")
def project_has_config_layer(project, config_layer):

    return [
        create_forward(project, has, f"{project.meta.term.data}:commands-dir"),
        create_forward(project, uses, ":dodo-menu"),
    ]


@rule("project", uses, "dodo-menu")
def project_uses_dodo_menu(project, dodo_menu):
    add(dodo_menu, dodo_layer_configs.get_for_menu(project))


@extend(Project)
class ExtendProject(StoreLayerConfigs):
    config_layer = P.child(has, "config:layer")
