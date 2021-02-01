from leapreact.component import Component
from moonleap import add, extend, render_templates, rule, tags
from moonleap.verbs import has, with_

from . import node_package_configs


class Router(Component):
    pass


@tags(["router"])
def create_router(term, block):
    router = Router(name="UrlRouter", import_path="")
    add(router, node_package_configs.get())
    return router


@rule("app:module", has, "router")
def service_has_router(app_module, router):
    app_module.add_component(router)


@extend(Router)
class ExtendRouter:
    render = render_templates(__file__)
