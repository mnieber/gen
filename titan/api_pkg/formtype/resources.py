from dataclasses import dataclass

from moonleap import Resource


@dataclass
class FormType(Resource):
    name: str
    name_snake: str
