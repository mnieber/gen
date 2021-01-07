import json

import moonleap.props as props
import ramda as R
from leap_mn.layergroup import LayerGroup
from moonleap import Resource, tags
from yaml import dump


class Layer(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Layer name={self.name}"

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )


class LayerConfig(Resource):
    def __init__(self, name, config):
        super().__init__()
        self.name = name
        self._config = config

    @property
    def config(self):
        body = self._config(self) if callable(self._config) else self._config
        return {self.name.upper(): body}

    @property
    def as_yaml(self):
        return dump(self.config)


@tags(["layer"])
def create_layer(term, block):
    return [Layer(name=term.data)]


meta = {
    Layer: dict(
        templates="templates",
        output_dir=".dodo_commands",
        props={
            "parent_layer_group": props.parent_of_type(LayerGroup),
            "sections": props.children_of_type(
                LayerConfig, sort=R.sort_by(R.prop("name"))
            ),
            "layer_groups": props.children_of_type(LayerGroup),
        },
    ),
    LayerConfig: dict(
        props={
            "layer": props.parent_of_type(Layer),
        },
    ),
}
