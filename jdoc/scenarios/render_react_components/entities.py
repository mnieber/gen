from jdoc.scenarios.imports import *

# Moonleap entities
actions = Actions()
blocks = Blocks()
entry_point = EntryPoint()
expanded_markdown = ExpandedMarkdown()
settings = Settings()
source_code = SourceCode()

# Moonleap functions
build_blocks = BuildBlocksFn()
generate_code = GenerateCodeFn()
run_actions = RunActionsFn()

# Titan entities
default_package = Package(name="default")
default_scope = Scope(name="default")
react_package = Package(name="react")

# TodoApp entities
frontend_service = ServiceRes(name="frontend")
frontend_service_block = Block(name="frontend-service")
frontend_service_scope = Scope(name="frontend-service")
main_block = Block(name="main")
todo_view_res = ReactComponent(name="todo-:view")

# Rules
assign_components_to_react_modules = Rule(
    name="assign_components_to_react_modules", pattern='@rule("react-app")'
)

# Relations
component_is_created = create_relation("component", "/is-created-as", "component")
react_app_is_created = create_relation("react-app", "/is-created-as", "react-app")
todos_module_has_todos_view = create_relation("todos:module", "/has", "todos:view")
