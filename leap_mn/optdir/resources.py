from dataclasses import dataclass

from moonleap.resource import Resource


@dataclass
class OptPath(Resource):
    is_dir: bool
    from_path: str
    to_path: str


@dataclass
class OptDir(Resource):
    pass
