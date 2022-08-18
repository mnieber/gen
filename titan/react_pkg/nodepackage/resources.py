from dataclasses import dataclass

from moonleap import Resource
from titan.project_pkg.service import Tool


@dataclass
class NodePackage(Tool):
    pass


@dataclass
class Pkg(Resource):
    name: str
