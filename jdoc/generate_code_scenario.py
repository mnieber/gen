from dataclasses import dataclass

from pipeop import pipes

from jdoc.blocks import *
from jdoc.resource import *
from jdoc.spec_markdown import *
from jdoc.verbs import *


class GetBlocksFn(Entity):
    def get_blocks(self, expanded_markdown: ExpandedMarkdown, blocks: Blocks):
        get_blocks_fn = self
        infos = [
            f"💡The {get_blocks_fn.t} adds :lines to each :block. "
            #
        ]

        blocks.main_block = MainBlock()
        blocks.main_block.fake_get_lines_from_expanded_markdown(expanded_markdown)

        blocks.backend_service_block = BackendServiceBlock()
        blocks.backend_service_block.fake_get_lines_from_expanded_markdown(
            expanded_markdown
        )

        infos += [
            f"""
💡The {get_blocks_fn.t} reads the :scope names from the :block name in the
{expanded_markdown.t}. It looks up the :scopes in the {global_settings.t} and
adds them to the :block.
            """
        ]

        blocks.main_block.fake_get_scopes_from_settings()
        blocks.backend_service_block.fake_get_scopes_from_settings()

        return infos


@dataclass
class BuildBlocksFn(Entity):
    def build_blocks(self, blocks: Blocks):
        build_blocks_fn = self
        infos = [
            f"💡The {build_blocks_fn.t} creates :relations in each :block. "
            #
        ]

        blocks.main_block.fake_get_relations()
        blocks.backend_service_block.fake_get_relations()

        return infos


@dataclass
class ProcessRelationsFn(Entity):
    block_that_describes_the_foo_project: Block = None
    block_that_describes_docker_compose: Block = None
    block_that_describes_the_backend_service: Block = None
    block_that_describes_pip_compile: Block = None

    def process_relations(self, blocks: Blocks):
        process_relations_fn = self
        infos = [
            f"💡The {process_relations_fn.t} creates :resources for the terms (the "
            + f"subject and object) in the :relations of each :block. "
            + f"For every :term in a :block B, it tries to find the resource in the "
            + f"competing:blocks of that :block. If not found, then it determines "
            + f"the competing:block that describes the :term. In that block, it finds "
            + f"scope that has the :create-rule for that :term, and runs this :rule."
            + f"Finally, it adds the created :resource to the describing :block, and "
            + f"also to the original block B."
            #
        ]

        # Here, we fake finding the block that describes each term.
        self.block_that_describes_the_foo_project = blocks.main_block
        self.block_that_describes_docker_compose = blocks.main_block
        self.block_that_describes_the_backend_service = blocks.backend_service_block
        self.block_that_describes_pip_compile = blocks.backend_service_block

        infos = [
            f"💡When {process_relations_fn.t} processes a relation in a block B, "
            + f"then it also finds all matching relation:rules in all :scopes of B. "
            + f"For every matching relation:rule, it creates an :action. "
            + f"It returns the list with all created :actions."
            #
        ]

        # Here, we fake the resource look-up/creation process, by just requesting the
        # resources directly using fake_look_up_res_in_competing_blocks.
        # We also fake the creation of actions by just calling
        # fake_create_actions_for_matching_rules().
        blocks.actions = Actions()
        for rel in (
            blocks.main_block.foo_project_uses_docker_compose,
            blocks.main_block.docker_compose_runs_backend_service,
            blocks.backend_service_block.backend_service_uses_pip_compile,
        ):
            rel.subj_res = fake_look_up_res_in_competing_blocks(rel.subj, blocks)
            rel.obj_res = fake_look_up_res_in_competing_blocks(rel.obj, blocks)
            rel.fake_create_actions_for_matching_rules(blocks.actions)

        return infos


@dataclass
class RunActionsFn(Entity):
    def run_actions(self, actions: Actions):
        infos = [
            """The run_actions() function runs the rule of each action in the
            actions list. Note that the rule may return "retry", and in that case
            the action is re-added to the end of the list. This mechanism helps
            to run some of the rules in the right order.
            """
        ]

        # Here, we fake running the actions.
        for action in actions.actions:
            forwards = Forwards()
            infos += action.rule.run(action.src_rel, forwards)
            if forwards.relations:
                # In the real system, we would process the forwarded relations
                pass

        return infos


render_resources_snippet = """
VERSION.txt.j2:
    name: "VERSION-{{ _.version_nr }}.txt"
    include: {{ _.has_flag("app/useVersioning")|bool }}
"""


@dataclass
class RenderResourcesFn(Entity):
    def render_resources(self, root_resource: RootResource, source_code: SourceCode):
        infos = []

        # Here, we fake the rendering cascade.
        queue = [
            RenderTask(
                resource=root_resource,
                output_path=".",
                render_context=RenderContext(),
                template_dirs=[],
            )
        ]
        while queue:
            render_task = queue.pop()
            render_meta_data = RenderMetaData(contents=render_resources_snippet)
            render_helpers = RenderHelpers()

            if not infos:
                infos = [
                    f"""
When a resource is rendered, we iterate over the template directories and render the
templates using the {render_task.render_context.t} and {render_helpers.t}.
The output filename is based on the template filename (with the ".j2" extension
removed), but the {render_meta_data.t} may stipulate a different output filename.
The {render_meta_data.t} may also stipulate that the template is skipped.
The {render_helpers.t} are loaded from the '__moonleap__.py' file in the template
directory.
            """,
                    f"""
The {global_file_writer.t} is used to write the rendered files to disk. If the output
is the same as it was in the previous run, then the file-writer may leave the output
file untouched (this is explained in the documentation on syncing the shadow project
with the real project).
                    """,
                    f"""
When the resource has been rendered, then the rendering cascade continues with the
:render-tasks that are stored in the resource. In this case, the rendering context
is passed down; in other words, the rendering context gets bigger and bigger as we
descend the rendering cascade. This allows us to use "upstream resources" when rendering
a "down-stream resource". Similarly, the output directory from the upstream resource is
passed down; this means that a downstream resource is rendered in a subdirectory
of the upstream resource.
                    """,
                ]

            infos += render_task.resource.fake_render(
                global_file_writer,
                render_task.render_context,
                render_helpers,
                render_meta_data,
            )
            queue += render_task.resource.render_tasks

        return infos


@dataclass
class PostProcessSourceCodeFn(Entity):
    def post_process_source_code(
        self, source_code: SourceCode, file_writer: FileWriter
    ):
        post_process_source_code_fn = self
        infos = [
            f"""
The {post_process_source_code_fn.t} iterates over all files written by the {file_writer.t}.
For every file, it look up the related formatters in the {global_settings.t} and runs them.
            """
        ]

        return infos


@dataclass
class GenerateCodeFn(Entity):
    raw_markdown = RawMarkdown()
    expanded_markdown = ExpandedMarkdown()
    blocks = Blocks()

    expand_markdown_fn = ExpandMarkdownFn()
    get_blocks_fn = GetBlocksFn()
    build_blocks_fn = BuildBlocksFn()
    process_relations_fn = ProcessRelationsFn()
    run_actions_fn = RunActionsFn()
    render_resources_fn = RenderResourcesFn()
    post_process_source_code_fn = PostProcessSourceCodeFn()


@pipes
def f001(s: Scenario, f: tuple[GenerateCodeFn, generates_, SourceCode]):
    generate_code = get(f, GenerateCodeFn)
    source_code = get(f, SourceCode)
    gc = generate_code

    raw_markdown = generate_code.raw_markdown
    expanded_markdown = generate_code.expanded_markdown

    with s.add_fact(f):
        f002(s, (generate_code, reads_(), raw_markdown))
        f003(
            s, (gc.expand_markdown, expands_(), raw_markdown, to_(), expanded_markdown)
        )

    blocks = generate_code.blocks

    with s.add_fact(f):
        f004(s, (gc.get_blocks_fn, transforms_(), expanded_markdown, to_(), blocks))
        f005(s, (gc.build_blocks_fn, builds_(), blocks))
        f006(s, (gc.process_relations_fn, processes_(), blocks))
        f007(s, (gc.run_actions_fn, runs_(), blocks.actions))
        f008(
            s,
            (
                gc.render_resources_fn,
                renders_(),
                global_root_resource,
                to_(),
                source_code,
            ),
        )
        f009(
            s,
            (gc.post_process_source_code_fn, post_processes_(), source_code),
        )


@pipes
def f002(s: Scenario, f: tuple[GenerateCodeFn, reads_, RawMarkdown]):
    s.add_fact(f)


@pipes
def f003(
    s: Scenario,
    f: tuple[ExpandMarkdownFn, expands_, RawMarkdown, to_, ExpandedMarkdown],
):
    expand_markdown = get(f, ExpandMarkdownFn)
    raw_markdown = get(f, RawMarkdown)
    expanded_markdown = get(f, ExpandedMarkdown)

    with s.add_fact(f):
        expand_markdown.expand_markdown(raw_markdown, expanded_markdown) >> s.add_infos


@pipes
def f004(
    s: Scenario,
    f: tuple[GetBlocksFn, transforms_, ExpandedMarkdown, to_, Blocks],
):
    get_blocks = get(f, GetBlocksFn)
    expanded_markdown = get(f, ExpandedMarkdown)
    blocks = get(f, Blocks)

    with s.add_fact(f):
        get_blocks.get_blocks(expanded_markdown, blocks) >> s.add_infos


@pipes
def f005(
    s: Scenario,
    f: tuple[BuildBlocksFn, builds_, Blocks],
):
    build_blocks_fn = get(f, BuildBlocksFn)
    blocks = get(f, Blocks)

    with s.add_fact(f):
        build_blocks_fn.build_blocks(blocks) >> s.add_infos


@pipes
def f006(
    s: Scenario,
    f: tuple[ProcessRelationsFn, processes_, Blocks],
):
    process_relations_fn = get(f, ProcessRelationsFn)
    blocks = get(f, Blocks)

    with s.add_fact(f):
        process_relations_fn.process_relations(blocks) >> s.add_infos


@pipes
def f007(
    s: Scenario,
    f: tuple[RunActionsFn, runs_, Actions],
):
    run_actions_fn = get(f, RunActionsFn)
    actions = get(f, Actions)

    with s.add_fact(f):
        run_actions_fn.run_actions(actions) >> s.add_infos


@pipes
def f008(
    s: Scenario,
    f: tuple[RenderResourcesFn, renders_, RootResource, to_, SourceCode],
):
    render_resources_fn = get(f, RenderResourcesFn)
    source_code = get(f, SourceCode)
    root_resource = get(f, RootResource)

    with s.add_fact(f):
        render_resources_fn.render_resources(root_resource, source_code) >> s.add_infos


@pipes
def f009(
    s: Scenario,
    f: tuple[PostProcessSourceCodeFn, post_processes_, SourceCode],
):
    post_process_source_code_fn = get(f, PostProcessSourceCodeFn)
    source_code = get(f, SourceCode)

    with s.add_fact(f):
        (
            post_process_source_code_fn.post_process_source_code(
                source_code, global_file_writer
            )
            >> s.add_infos
        )


if __name__ == "__main__":
    s = Scenario()
    generate_code = GenerateCodeFn()
    source_code = SourceCode()

    f001(s, (generate_code, generates_(), source_code))
