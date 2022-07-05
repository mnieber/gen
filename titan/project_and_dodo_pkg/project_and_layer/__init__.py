import moonleap.resource.props as P
from moonleap import add, create_forward, extend, feeds, rule
from moonleap.verbs import has
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.project import Project

from . import dodo_config_layers

rules = [(("project", has, "config:layer"), feeds("dodo_layer_configs"))]


@rule("project", has, "config:layer")
def project_has_config_layer(project, config_layer):
    add(project, dodo_config_layers.get_for_project(project))

    return [create_forward(project, "has", f"{project.meta.term.data}:commands-dir")]


@extend(Project)
class ExtendProject(StoreLayerConfigs):
    config_layer = P.child(has, "config:layer")
