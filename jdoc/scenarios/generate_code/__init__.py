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
        add_info("Entry point loads settings")
        settings.scope_by_name = {
            "default": ["default"],
            "backend-service": ["default", "django"],
        }
        settings.post_process = {".ts(x)?": ["prettier"], ".py": ["black", "isort"]}
        settings.bin = {
            "black": {"exe": "~/.local/bin/black"},
            "isort": {"exe": "~/.local/bin/isort"},
            "prettier": {"exe": "~/.yarn/bin/prettier", "config": "~/.prettierrc"},
        }

        default_scope.packages = [default_package]
        backend_service_scope.packages = [default_package, django_package]


@pipes
def generate_source_code():
    #
    with (generate_code, generates_(), source_code) >> add_fact:
        #
        read_the_markdown_spec_file()
        transform_the_markdown_to_blocks()
        build_all_blocks()
        render_the_root_resource()
        post_process_the_generated_source_code()


@pipes
def read_the_markdown_spec_file():
    #
    with (generate_code, reads_(), raw_markdown) >> add_fact:
        #
        raw_markdown.contents = contents.raw_markdown

    with (
        generate_code,
        expands_(),
        raw_markdown,
        to_(),
        expanded_markdown,
    ) >> add_fact:
        #
        add_info("Fn generate_code() expands raw markdown")
        expanded_markdown.contents = contents.expanded_markdown


@pipes
def transform_the_markdown_to_blocks():
    #
    with (get_blocks, transforms_(), expanded_markdown, to_(), blocks) >> add_fact:
        #
        blocks.blocks = [main_block, backend_service_block]
        main_block.scopes = [default_scope]
        backend_service_block.scopes = [default_scope, backend_service_scope]


@pipes
def build_all_blocks():
    #
    with (build_blocks, builds_(), blocks) >> add_fact:
        #
        with (build_blocks, builds_(), main_block) >> add_fact:
            #
            main_block.relations = [
                todo_app_project_uses_docker_compose,
                docker_compose_runs_backend_service,
            ]

            with (process_relations, processes_(), main_block) >> add_fact:
                #
                todo_app_project_uses_docker_compose.subj_res = todo_app_project
                todo_app_project_uses_docker_compose.obj_res = docker_compose
                actions.actions += [
                    Action(
                        rule=root_resource_renders_project,
                        src_rel=todo_app_project_is_created,
                    ),
                    Action(
                        rule=project_renders_docker_compose_file,
                        src_rel=todo_app_project_uses_docker_compose,
                    ),
                ]

                docker_compose_runs_backend_service.subj_res = docker_compose
                docker_compose_runs_backend_service.obj_res = backend_service
                actions.actions += [
                    Action(
                        rule=service_adds_to_docker_compose_file,
                        src_rel=docker_compose_runs_backend_service,
                    ),
                ]

        with (build_blocks, builds_(), backend_service_block) >> add_fact:
            #
            backend_service_block.relations = [backend_service_uses_pip_compile]

            with (process_relations, processes_(), backend_service_block) >> add_fact:
                #
                backend_service_uses_pip_compile.subj_res = backend_service
                backend_service_uses_pip_compile.obj_res = pip_compile
                actions.actions = [
                    Action(
                        rule=service_runs_tool, src_rel=backend_service_uses_pip_compile
                    ),
                ]

        with (run_actions, runs_(), actions) >> add_fact:
            #
            root_resource.renders(todo_app_project)
            todo_app_project.renders(docker_compose)
            backend_service.renders(docker_compose)


@pipes
def render_the_root_resource():
    #
    with (render_resources, renders_(), root_resource, to_(), source_code) >> add_fact:
        #
        add_info("Render resources renders root resource")
        file_writer.files = [
            "docker-compose.yml",
        ]


@pipes
def post_process_the_generated_source_code():
    #
    with (post_process_output_files, post_processes_(), source_code) >> add_fact:
        #
        add_info("post_process_output_files post-processes source_code")
