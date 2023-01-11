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
widget_spec_parser = WidgetSpecParserRes()

# TodoApp entities
frontend_service = ServiceRes(name="frontend")
frontend_service_block = Block(name="frontend-service")
frontend_service_scope = Scope(name="frontend-service")
main_block = Block(name="main")
todo_view_res = ReactComponent(name="todo-:view")

# Rules
build_component_widget_spec = Rule(
    name="build_component_widget_spec",
    pattern='@rule("react-module", has, "component")',
)
create_forwards_for_component_pipelines = Rule(
    name="create_forwards_for_component_pipelines", pattern="@rule('component')"
)
create_forwards_for_component_props = Rule(
    name="create_forwards_for_component_props", pattern="@rule('component')"
)
assign_components_to_react_modules = Rule(
    name="assign_components_to_react_modules", pattern='@rule("react-app")'
)

# Relations
component_is_created = create_relation("component", "/is-created-as", "component")
react_app_is_created = create_relation("react-app", "/is-created-as", "react-app")
todos_module_has_todos_view = create_relation("todos:module", "/has", "todos:view")

# Widget specs
todo_view_widget_spec = WidgetSpec(
    module_name="todos",
    component_term="todo-:view",
    widget_base_types=["Div"],
    child_widget_specs=[
        WidgetSpec(
            module_name="todos",
            component_term="todo-form-:view",
        )
    ],
)
