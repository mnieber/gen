from jdoc.scenario import *

if T.TYPE_CHECKING:
    from jdoc.packages import *
    from jdoc.resources import Resource


@dataclass
class Resource(Entity):
    render_tasks: list["RenderTask"] = field(default_factory=list)

    def renders(self, render_task: "RenderTask"):
        self.render_tasks += [render_task]

    def fake_render(
        self,
        file_writer: "FileWriter",
        render_context: "RenderContext",
        render_helpers: "RenderHelpers",
        render_meta_data: "RenderMetaData",
    ):
        return []


@dataclass
class RootResource(Resource):
    pass


global_root_resource = RootResource()


@dataclass
class SourceCode(Entity):
    pass


@dataclass
class FileWriter(Entity):
    pass


global_file_writer = FileWriter()


@dataclass
class RenderHelpers(Entity):
    pass


@dataclass
class RenderContext(Entity):
    pass


@dataclass
class RenderMetaData(Entity):
    contents: str


@dataclass
class RenderTask(Entity):
    resource: "Resource"
    output_path: str
    render_context: RenderContext
    template_dirs: list
