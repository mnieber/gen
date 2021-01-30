from dataclasses import dataclass

from leaptools.tool import Tool
from moonleap.resource import Resource


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
