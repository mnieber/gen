from pipeop import pipes

from jdoc.blocks import *
from jdoc.generate_code_scenario import BuildBlocksFn
from jdoc.packages import *
from jdoc.scenario import *
from jdoc.type_reg import *
from jdoc.widget_reg import *


@dataclass
class FrontendServiceRes(Resource):
    pass


@dataclass
class ReactAppRes(Resource):
    pass


@dataclass
class ReactTodosModuleRes(Resource):
    pass


@dataclass
class TodoViewRes(Resource):
    pass


react_app_res = ReactAppRes()
react_todos_module_res = ReactTodosModuleRes()
todo_view_res = TodoViewRes()


def fake_look_up_res_in_competing_blocks(term):
    return (
        react_app_res
        if term == "react-app"
        else react_todos_module_res
        if term == "react-todos-module"
        else todo_view_res
        if term == "todo:view"
        else None
    )


@dataclass
class FrontendServiceBlock(Block):
    def fake_run_creation_rules(self, rel: Relation):
        # Here, we fake the creation of the resources for 'rel'. and
        rel.subj_res = fake_look_up_res_in_competing_blocks(rel.subj)
        rel.obj_res = fake_look_up_res_in_competing_blocks(rel.obj)


class ReactModuleHasComponentRule(Rule):
    pattern: str = '@rule("react-module", has, "component")'

    def run(self, rel: "Relation", forwards: "Forwards"):
        infos = []
        react_module, component = rel.subj_res, rel.obj_res
        react_module.renders(
            RenderTask(
                resource=component,
                output_path="components",
                render_context=dict(component=component),
                template_dirs=[],
            )
        )
        return infos


global_react_module_has_component_rule = ReactModuleHasComponentRule()


class ReactModulesHaveComponentsRule(Rule):
    pattern: str = '@rule("react-app")'
    name: str = "react_modules_have_components"

    def run(self, rel: "Relation", forwards: "Forwards"):
        react_modules_have_components_rule = self
        infos = [
            f"""
The {react_modules_have_components_rule.t} iterates over all the :widget-specs in the
{global_widget_reg.t}. For every :widget-spec it creates forward relations that
stipulate that a particular react-module defines the component.
            """
        ]

        global_widget_reg.load_widget_specs()
        for widget_spec in global_widget_reg.widget_specs:
            forwards.relations += [
                create_relation(
                    f"{widget_spec.module_name}:react-module",
                    "has",
                    "{widget_spec.component_term}",
                )
            ]
        return infos


global_react_modules_have_components_rule = ReactModulesHaveComponentsRule()


@pipes
def f001(
    s: Scenario,
    f: tuple[BuildBlocksFn, builds_, FrontendServiceBlock],
):
    build_blocks_fn = get(f, BuildBlocksFn)
    frontend_service_block = get(f, FrontendServiceBlock)
    frontend_service_uses_react_app = create_relation(
        "frontend-service", "uses", "react-app"
    )

    with s.add_fact(f):
        # Here, we fake the addition of the "frontend-service /uses react-app"
        # relation to the frontend_service_block
        frontend_service_block.fake_run_creation_rules(frontend_service_uses_react_app)

        # Here we fake the processing of frontend_service_uses_react_app by a rule.
        # This rule returns a forward relation: todos_module_has_todo_view.
        forwards = Forwards()
        infos = global_react_modules_have_components_rule.run(
            frontend_service_uses_react_app, forwards
        )
        s.add_infos(infos)

        # Here we fake the processing of the forwarded relation by a rule.
        todos_module_has_todo_view = forwards.relations[0]
        frontend_service_block.fake_run_creation_rules(todos_module_has_todo_view)

        # Here we fake the processing of todos_module_has_todo_view by a rule.
        infos = global_react_module_has_component_rule.run(
            todos_module_has_todo_view, Forwards()
        )
        s.add_infos(infos)


# @pipes
# def f002(
#     s: Scenario,
#     f: tuple[BuildBlocksFn, runs_, ReactModulesHaveComponentsRule],
# ):
#     build_blocks_fn = get(f, BuildBlocksFn)

#     with s.add_fact(f):


if __name__ == "__main__":
    s = Scenario()

    build_blocks_fn = BuildBlocksFn()
    frontend_service_block = FrontendServiceBlock()
    blocks = Blocks()
    source_code = SourceCode()

    f001(s, (build_blocks_fn, builds_(), frontend_service_block))
