import moonleap.resource.props as P
from moonleap import add, add_source, extend, rule
from moonleap.verbs import has
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.project import Project

from . import config_layers


@rule("project", has, "config:layer")
def project_has_config_layer(project, config_layer):
    add(project, config_layers.get(project))
    add_source(
        [config_layer, "layer_configs"],
        project,
        "The config:layer receives layer configs from the :project",
    )


@extend(Project)
class ExtendProject(StoreLayerConfigs):
    config_layer = P.child(has, "config:layer")
