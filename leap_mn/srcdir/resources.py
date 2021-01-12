from dataclasses import dataclass

from moonleap import Resource


@dataclass
class SrcDir(Resource):
    location: str
