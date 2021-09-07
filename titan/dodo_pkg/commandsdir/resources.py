from dataclasses import dataclass

from moonleap import Resource


@dataclass
class CommandsDir(Resource):
    name: str
