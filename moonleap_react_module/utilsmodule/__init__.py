import moonleap.resource.props as P
from moonleap import extend
from moonleap.verbs import has
from moonleap_project.service import Service


@extend(Service)
class ExtendService:
    utils_module = P.child(has, "utils:module")
