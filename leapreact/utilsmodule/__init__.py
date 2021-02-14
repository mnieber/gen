import moonleap.resource.props as P
from leapproject.service import Service
from leapreact.module import create_module
from moonleap import Term, extend
from moonleap.verbs import has


def create_utils_module(service):
    if not service.utils_module:
        service.utils_module = create_module(Term(data="utils", tag="module"), None)
    return service.utils_module


@extend(Service)
class ExtendService:
    utils_module = P.child(has, "utils:module")
