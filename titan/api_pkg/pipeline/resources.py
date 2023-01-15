from dataclasses import dataclass, field

from moonleap import Resource

from . import props


@dataclass
class Pipeline:
    name: str
    resources: list[Resource] = field(default_factory=list)

    def data_path(self, obj):
        return props.pipeline_data_path(self, obj)

    def maybe_expression(self, named_item_or_item_list):
        return props.pipeline_maybe_expression(self, named_item_or_item_list)

    @property
    def source(self):
        return props.pipeline_source(self)


@dataclass
class PropsSource(Resource):
    pass


@dataclass
class LocalVars(Resource):
    pass
