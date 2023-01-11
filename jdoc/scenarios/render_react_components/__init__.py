from pipeop import pipes

from jdoc.scenarios.imports import *

from . import contents
from .entities import *
from .scenario import add_fact, add_info


@pipes
def load_settings():
    #
    with (entry_point, loads_(), settings) >> add_fact:
        #
        settings.scope_by_name = {
            "default": ["default"],
            "frontend-service": ["default", "react"],
        }

        default_scope.packages = [default_package]
        frontend_service_scope.packages = [default_package, react_package]


@pipes
def generate_source_code():
    #
    with (generate_code, generates_(), source_code) >> add_fact:
        #
        build_all_blocks()


@pipes
def build_all_blocks():
    #
    with (build_blocks, builds_(), blocks) >> add_fact:
        #
        expanded_markdown.contents = contents.expanded_markdown
        blocks.blocks = [main_block, frontend_service_block]

        with (build_blocks, builds_(), frontend_service_block) >> add_fact:
            #
            actions.actions += [
                Action(
                    rule=assign_components_to_react_modules,
                    src_rel=react_app_is_created,
                ),
                Action(
                    rule=create_forwards_for_component_pipelines,
                    src_rel=component_is_created,
                ),
                Action(
                    rule=create_forwards_for_component_props,
                    src_rel=component_is_created,
                ),
                Action(
                    rule=build_component_widget_spec,
                    src_rel=component_is_created,
                ),
            ]

        with (
            run_actions,
            runs_(),
            assign_components_to_react_modules,
        ) >> add_fact:
            #
            add_info("Components are assigned to react-modules")
            widget_spec_parser.widget_spec_yaml = contents.widget_spec_todos_yaml

        with (
            run_actions,
            runs_(),
            create_forwards_for_component_pipelines,
        ) >> add_fact:
            #
            add_info("A component has pipelines")

        with (run_actions, runs_(), build_component_widget_spec) >> add_fact:
            #
            add_info("Fn build() builds a widget_spec")
