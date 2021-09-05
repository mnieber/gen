from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Form(Resource):
    item_name: str
    item_name_snake: str

    @property
    def data_type_name(self):
        return self.item_name + "Form"
