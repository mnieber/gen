from leapreact.reacttool import ReactTool
from moonleap import add, extend, render_templates, rule, tags
from moonleap.verbs import with_

from . import node_package_configs


class Router(ReactTool):
    pass


@tags(["router"])
def create_router(term, block):
    router = Router()
    add(router, node_package_configs.get())
    return router


@rule("create-react-app", with_, "router")
def cra_with_router(cra, router):
    cra.node_package_configs.add_source(router)
    router.output_paths.add_source(cra)


@extend(Router)
class ExtendRouter:
    render = render_templates(__file__, "templates/UrlRouter.tsx")
