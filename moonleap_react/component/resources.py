from dataclasses import dataclass

from moonleap.resource import Resource
from moonleap_tools.tool import Tool


@dataclass
class Component(Tool):
    name: str
    import_path: str

    @property
    def var_name(self):
        return self.name[0].lower() + self.name[1:]


@dataclass
class JavascriptImport(Resource):
    paths: [str]


@dataclass
class CssImport(Resource):
    paths: [str]
