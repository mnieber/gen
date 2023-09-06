from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Div(Resource):
    classnames: [str] = field(default_factory=list)
