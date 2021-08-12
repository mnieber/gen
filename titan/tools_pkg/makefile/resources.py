from dataclasses import dataclass

from titan.project_pkg.service import Tool
from moonleap import Resource


@dataclass
class Makefile(Tool):
    pass


@dataclass
class MakefileRule(Resource):
    text: str
