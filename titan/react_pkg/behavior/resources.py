import typing as T
from dataclasses import dataclass

from moonleap import Resource, u0
from moonleap.utils.case import kebab_to_camel


@dataclass
class Behavior(Resource):
    # This is the full facet name, e.g. DeletionWithFlag
    name: str
    # This is the optional interface name, e.g. IDeletionWithFlag
    has_param: bool
    is_skandha: bool = True
    interface_name: T.Optional[str] = None

    @property
    def facet_name(self):
        return u0(kebab_to_camel(self.meta.term.parts[-2]))

    @property
    def mutation(self):
        return None


def is_exposed_bvr(bvr):
    return bvr.facet_name not in ("Store", "Display")
