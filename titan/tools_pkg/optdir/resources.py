from dataclasses import dataclass

from moonleap.resource import Resource
from titan.project_pkg.service import Tool


@dataclass
class OptPath(Resource):
    is_dir: bool
    from_path: str
    to_path: str


@dataclass
class OptDir(Tool):
    pass
