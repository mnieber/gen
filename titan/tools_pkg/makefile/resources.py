from dataclasses import dataclass

from moonleap import Resource
from titan.project_pkg.service import Tool


@dataclass
class Makefile(Tool):
    pass


@dataclass
class MakefileRule(Resource):
    name: str
    text: str
