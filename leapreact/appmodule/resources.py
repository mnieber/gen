from dataclasses import dataclass

from leaptools.tool import Tool
from moonleap import Resource


@dataclass
class AppModule(Tool):
    name: str


@dataclass
class CssImport(Resource):
    paths: [str]
