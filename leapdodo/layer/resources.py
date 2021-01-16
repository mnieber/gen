import typing as T
from dataclasses import dataclass

from moonleap import Resource
from moonleap.utils.uppercase_dict_keys import uppercase_dict_keys


@dataclass
class Layer(Resource):
    name: str

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )


@dataclass
class LayerConfig(Resource):
    body: T.Union[dict, T.Callable]

    def __repr__(self):
        return f"LayerConfig name={self.name}"

    @property
    def name(self):
        return "/".join(self.get_body().keys())

    def get_body(self):
        body = self.body() if callable(self.body) else self.body
        return uppercase_dict_keys(body)
