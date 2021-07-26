from dataclasses import dataclass

from moonleap_project.service import Tool
from moonleap import Resource


@dataclass
class Makefile(Tool):
    pass


@dataclass
class MakefileRule(Resource):
    text: str
