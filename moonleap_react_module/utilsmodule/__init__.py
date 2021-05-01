import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.render.storetemplatedirs import add_template_dir
from moonleap.verbs import has
from moonleap_project.service import Service


@rule("service", has, "utils:module")
def service_has_utils_module(service, utils_module):
    utils_module.add_template_dir(__file__, "templates")


@extend(Service)
class ExtendService:
    utils_module = P.child(has, "utils:module")
