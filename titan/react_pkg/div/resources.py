from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Div(Resource):
    name: str
    classnames: [str] = field(default_factory=list)
