import os
from pathlib import Path

from moonleap.block_builder.build_blocks import build_blocks
from moonleap.entrypoint.sync_files import sync_files
from moonleap.render.post_process_output_files import post_process_output_files
from moonleap.render.remove_stale_output_files import remove_stale_output_files
from moonleap.render_queue.add_render_tasks_from_packages import (
    add_render_tasks_from_packages,
)
from moonleap.render_queue.process_render_queue import process_render_queue
from moonleap.report.report_resources import report_resources
from moonleap.session import trace
from moonleap.spec_parser.expand_markdown import expand_markdown
from moonleap.spec_parser.get_blocks import get_blocks


def generate_code(session, post_process_all_files):
    expanded_markdown = expand_markdown(
        session.ws.spec_fn, output_fn=Path(".moonleap") / "spec.md"
    )

    trace("Parsing...")
    blocks = get_blocks(expanded_markdown)
    build_blocks(blocks)

    try:
        trace("Rendering...")
        trace("Rendering root resource", 1)
        add_render_tasks_from_packages(session.settings.get("packages_by_scope", {}))
        process_render_queue()

        file_writer = session.ws.file_writer
        file_writer.write_merged_files()
        for warning in file_writer.warnings:
            trace(warning)

        trace("Post processing...")
        post_process_output_files(
            (
                file_writer.all_output_filenames
                if post_process_all_files
                else file_writer.output_filenames
            ),
            session.get_post_process_settings(),
            session.get_bin_settings(),
        )
    except Exception as e:
        raise e
    else:
        file_writer.write_snapshot()
        remove_stale_output_files(
            file_writer.all_output_filenames, session.ws.output_dir
        )
        sync_files(
            session.ws.output_dir,
            os.path.join(session.ws.output_root_dir, "shadow"),
            os.path.join(session.ws.output_root_dir, "stage"),
        )

    trace("Creating report...")
    report_resources(blocks)
