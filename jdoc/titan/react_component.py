import typing as T

from jdoc.titan.imports import *
from jdoc.titan.widget_reg import *


class Pipeline(Resource):
    component: "ReactComponent" = None
    resources: T.List[Resource] = []

    def source(self) -> Resource:
        pass

    def data_path(self, obj: Resource) -> str:
        pass


class ReactComponent(Resource):
    name: str = ""
    pipelines: T.List[Pipeline] = []
    props: T.List[Resource] = []
    widget_spec: WidgetSpec = None
