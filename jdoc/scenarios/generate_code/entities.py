from jdoc.moonleap.blocks import ProcessRelationsFn
from jdoc.scenarios.imports import *

from . import contents

# Moonleap entities
actions = Actions()
blocks = Blocks()
entry_point = EntryPoint()
expanded_markdown = ExpandedMarkdown()
file_writer = FileWriter()
raw_markdown = RawMarkdown()
render_helpers = RenderHelpers()
render_meta_data = RenderMetaData(contents=contents.render_resources_snippet)
root_resource = RootResource()
settings = Settings()
source_code = SourceCode()

# Moonleap functions
generate_code = GenerateCodeFn()
expand_markdown = ExpandMarkdownFn()
get_blocks = GetBlocksFn()
build_blocks = BuildBlocksFn()
process_relations = ProcessRelationsFn()
run_actions = RunActionsFn()
render_resources = RenderResourcesFn()
post_process_output_files = PostProcessOutputFilesFn()

# Titan entities
default_package = Package(name="default")
default_scope = Scope(name="default")
django_package = Package(name="django")
docker_compose = DockerComposeRes()
pip_compile = PipCompileRes()

# TodoApp entities
backend_service = ServiceRes(name="backend")
backend_service_block = Block(name="backend-service")
backend_service_scope = Scope(name="backend-service")
main_block = Block(name="main")
todo_app_project = ProjectRes(name="todo-app")

# Relations
todo_app_project_is_created = create_relation(
    "todo-app:project", "/is-created-as", "todo-app:project"
)
todo_app_project_uses_docker_compose = create_relation(
    "todo-app:project", "/uses", ":docker-compose"
)
docker_compose_runs_backend_service = create_relation(
    ":docker-compose", "/runs", "backend:service"
)
backend_service_uses_pip_compile = create_relation(
    "backend:service", "/uses", ":pip-compile"
)

# Rules
root_resource_renders_project = Rule(
    name="root_resource_renders_project", pattern="@rule('project')"
)
project_renders_docker_compose_file = Rule(
    name="project_renders_docker_compose_file",
    pattern="@rule('project', uses, 'docker-compose')",
)
service_adds_to_docker_compose_file = Rule(
    name="service_adds_to_docker_compose_file",
    pattern="@rule('docker-compose', runs, 'service')",
)
service_runs_tool = Rule(
    name="service_runs_tool", pattern="@rule('service', runs, 'tool')"
)
