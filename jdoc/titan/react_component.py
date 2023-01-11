from jdoc.titan.imports import *
from jdoc.titan.widget_reg import *


class Pipeline(Resource):
    component: "ReactComponent" = None
    resources: list[Resource] = []

    def source(self) -> Resource:
        pass

    def data_path(self, obj: Resource) -> str:
        pass


class ReactComponent(Resource):
    name: str = ""
    pipelines: list[Pipeline] = []
    props: list[Resource] = []
    widget_spec: WidgetSpec = None
