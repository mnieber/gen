from pathlib import Path

from moonleap import create_resources, get_blocks, report_resources
from moonleap.parser.expand_markdown import expand_markdown
from moonleap.render.post_process_output_files import post_process_output_files
from moonleap.render.render_template import render_template
from moonleap.render.storetemplatedirs import get_root_resource, render_resource


def generate_code(spec_file, session, file_writer, post_process_all_files):
    expanded_markdown = expand_markdown(spec_file)
    expanded_markdown_fn = Path(".moonleap") / "spec.md"

    if not expanded_markdown_fn.parent.exists():
        expanded_markdown_fn.parent.mkdir()

    with open(expanded_markdown_fn, "w") as f:
        f.write(expanded_markdown)

    session.report("Parsing...")
    blocks = get_blocks(expanded_markdown)
    create_resources(blocks)

    session.report("Rendering...")
    render_resource(
        get_root_resource(),
        write_file=file_writer.write_file,
        render_template=render_template,
        output_path="",
    )

    file_writer.write_merged_files()
    for warning in file_writer.warnings:
        session.report(warning)

    session.report("Creating report...")
    report_resources(blocks)

    session.report("Post processing...")
    post_process_output_files(
        file_writer.all_output_filenames
        if post_process_all_files
        else file_writer.output_filenames,
        session.get_post_process_settings(),
        session.get_bin_settings(),
    )

    file_writer.write_snapshot()
