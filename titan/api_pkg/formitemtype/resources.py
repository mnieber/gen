from dataclasses import dataclass

from moonleap import Resource


@dataclass
class FormItemType(Resource):
    name: str
    name_snake: str
