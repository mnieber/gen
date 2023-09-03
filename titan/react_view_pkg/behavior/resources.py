from dataclasses import dataclass

from moonleap import Resource
from moonleap.utils.case import kebab_to_camel


@dataclass
class Behavior(Resource):
    name: str
    has_param: bool
    is_skandha: bool = True

    @property
    def facet_name(self):
        return kebab_to_camel(self.meta.term.parts[-2])

    @property
    def mutation(self):
        return None
