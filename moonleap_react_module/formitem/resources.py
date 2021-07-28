from dataclasses import dataclass

from moonleap import Resource


@dataclass
class FormItem(Resource):
    item_name: str
