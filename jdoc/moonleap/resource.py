import typing as T

from jdoc.moonleap.imports import *


class RenderContext(Entity):
    pass


class Resource(Entity):
    render_tasks: T.List["RenderTask"] = []

    def renders(
        self,
        resource: "Resource",
        output_path: str = ".",
        render_context: RenderContext = factory(RenderContext),
        template_dirs: T.List[str] = [],
    ):
        self.render_tasks += [
            RenderTask(
                resource=resource,
                output_path=output_path,
                render_context=render_context,
                template_dirs=template_dirs,
            )
        ]


class RootResource(Resource):
    pass


class SourceCode(Entity):
    pass


class FileWriter(Entity):
    pass


class RenderHelpers(Entity):
    pass


class RenderMetaData(Entity):
    contents: str


class RenderTask(Entity):
    resource: "Resource" = None
    output_path: str = ""
    render_context: RenderContext = None
    template_dirs: list = []
