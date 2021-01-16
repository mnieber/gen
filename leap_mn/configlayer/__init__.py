import moonleap.resource.props as P
from leap_mn.layer import Layer, LayerConfig
from leap_mn.project import Project
from moonleap import extend, rule, tags

from .layer_configs import get_root_config


@tags(["config:layer"])
def create_layer(term, block):
    layer = Layer(name="config")
    layer.layer_configs.add(LayerConfig(get_root_config()))

    return layer


@rule("project", "has", "config:layer")
def project_has_config_layer(project, config_layer):
    config_layer.layer_configs.add_source(project)


@extend(Project)
class ExtendProject:
    config_layer = P.child("has", "config:layer", is_doc=False)
