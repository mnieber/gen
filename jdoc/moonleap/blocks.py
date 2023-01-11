from jdoc.moonleap.block import *
from jdoc.moonleap.imports import *
from jdoc.moonleap.resource import *
from jdoc.moonleap.settings import *


class Blocks(Entity):
    blocks: list[Block] = []


class RawMarkdown(Entity):
    contents = ""


class ExpandedMarkdown(Entity):
    contents = ""


class ExpandMarkdownFn(Fn):
    name: str = "expand_markdown"

    def run(self, raw_markdown: RawMarkdown) -> ExpandedMarkdown:
        pass


class GetBlocksFn(Fn):
    name: str = "get_blocks"

    def run(self, expanded_markdown: ExpandedMarkdown) -> Blocks:
        pass


class BuildBlocksFn(Fn):
    name: str = "build_blocks"

    def run(self, blocks: Blocks):
        pass


class ProcessRelationsFn(Fn):
    name: str = "process_relations"

    def run(self, blocks: Blocks):
        pass


class RunActionsFn(Fn):
    name: str = "run_actions"

    def run(self, actions: Actions):
        pass


class RenderResourcesFn(Fn):
    name: str = "render_resources"

    def run(self, root_resource: RootResource):
        pass


class PostProcessOutputFilesFn(Fn):
    name: str = "post_process_output_files"

    def run(self, source_code: SourceCode):
        pass


class GenerateCodeFn(Fn):
    name: str = "generate_code"
