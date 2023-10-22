import os
from pathlib import Path

from moonleap.blocks.builder.build_blocks import build_blocks
from moonleap.blocks.parser.expand_markdown import expand_markdown
from moonleap.blocks.parser.get_blocks import get_blocks
from moonleap.entrypoint.gen.sync_files import sync_files
from moonleap.post_process import post_process_output_files
from moonleap.post_process.remove_stale_output_files import remove_stale_output_files
from moonleap.render.render_mixin import render_resource
from moonleap.render.render_queue.add_render_tasks_from_packages import (
    add_render_tasks_from_packages,
)
from moonleap.render.render_queue.process_render_queue import process_render_queue
from moonleap.render.root_resource import get_root_resource
from moonleap.report.report_resources import report_resources
from moonleap.session import trace


def generate_code(session, post_process_all_files):
    expanded_markdown = expand_markdown(
        session.spec_fn, output_fn=Path(".moonleap") / "spec.md"
    )

    trace("Parsing...")
    blocks = get_blocks(expanded_markdown)
    build_blocks(blocks)

    try:
        trace("Rendering...")
        trace("Rendering root resource", 1)
        root_resource = get_root_resource()
        render_resource(
            root_resource,
            write_file=session.file_writer.write_file,
            output_path="",
            context=dict(settings=session.settings),
        )

        add_render_tasks_from_packages(session.settings.get("packages_by_scope", {}))
        process_render_queue()

        session.file_writer.write_merged_files()
        for warning in session.file_writer.warnings:
            trace(warning)

        trace("Post processing...")
        post_process_output_files(
            session.file_writer.all_output_filenames
            if post_process_all_files
            else session.file_writer.output_filenames,
            session.get_post_process_settings(),
            session.get_bin_settings(),
        )
    except Exception as e:
        raise e
    else:
        session.file_writer.write_snapshot()
        remove_stale_output_files(
            session.file_writer.all_output_filenames, session.output_dir
        )
        sync_files(
            session.output_dir,
            os.path.join(session.output_root_dir, "shadow"),
            os.path.join(session.output_root_dir, "stage"),
        )

    trace("Creating report...")
    report_resources(blocks)
