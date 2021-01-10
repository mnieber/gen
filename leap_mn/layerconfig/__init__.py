import moonleap.props as props
import ramda as R
from leap_mn.layer import Layer
from moonleap import Resource
from moonleap.props import Prop
from moonleap.utils import merge_into_config


class LayerConfig(Resource):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def __str__(self):
        return f"LayerConfig name={self.name}"

    @property
    def name(self):
        layers = self.parents_of_type(Layer)
        return layers[0].name if len(layers) == 1 else ""

    def get_body(self):
        body = self.body(self) if callable(self.body) else self.body
        return R.pipe(
            R.always(body),
            R.to_pairs,
            R.map(lambda x: (x[0].upper(), x[1])),
            R.sort_by(lambda x: x[0]),
            R.from_pairs,
        )(None)


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(new_body)


def get_config():
    def prop(self):
        configs = self.children_of_type(LayerConfig)
        merged = R.reduce(merge, LayerConfig({}), configs)
        return merged.get_body()

    return Prop(prop, child_resource_type=LayerConfig)


def meta():
    return {
        Layer: dict(
            props={
                "config": get_config(),
            },
        ),
        LayerConfig: dict(
            props={
                "layer": props.parent_of_type(Layer),
            },
        ),
    }
