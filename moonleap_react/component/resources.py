from dataclasses import dataclass

from moonleap.resource import Resource
from moonleap_tools.tool import Tool


@dataclass
class Component(Tool):
    name: str


@dataclass
class JavascriptImport(Resource):
    paths: [str]


@dataclass
class CssImport(Resource):
    paths: [str]
