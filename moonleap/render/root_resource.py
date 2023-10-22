from dataclasses import dataclass

from moonleap.render.render_mixin import RenderMixin
from moonleap.resources.resource import Resource


@dataclass
class RootResource(RenderMixin, Resource):
    pass


_root_resource = None


def get_root_resource():
    global _root_resource
    if not _root_resource:
        _root_resource = RootResource()
    return _root_resource
