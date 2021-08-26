import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from moonleap import create_resources, get_blocks, render_resources, report_resources
from moonleap.parser.expand_markdown import expand_markdown
from moonleap.render.file_writer import FileWriter
from moonleap.render.post_process_output_files import post_process_output_files
from moonleap.report.create_expected_dir import create_expected_dir
from moonleap.report.diff import create_symlinks, diff
from moonleap.session import Session, set_session


def generate_code(spec_file, session):
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
    file_writer = FileWriter(session.snapshot_fn)
    render_resources(blocks, file_writer.write_file)
    for warning in file_writer.warnings:
        session.report(warning)
    file_writer.write_snapshot()

    session.report("Creating report...")
    report_resources(blocks)

    session.report("Post processing...")
    post_process_output_files(
        file_writer.output_filenames,
        session.settings.get("post_process", {}),
        session.settings.get("bin", {}),
    )


def report(x):
    print(x)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--spec", required=True, dest="spec_dir")
    parser.add_argument("--smart", required=False, action="store_true")
    parser.add_argument("--sudo", required=False, action="store_true")
    parser.add_argument("action", choices=["gen", "diff"])
    args = parser.parse_args()

    if args.smart and args.action != "diff":
        raise Exception("You can only use --smart with the 'diff' action")

    if args.sudo and args.action != "diff":
        raise Exception("You can only use --sudo with the 'diff' action")

    if not os.path.exists(args.spec_dir):
        report("Spec directory not found: " + args.spec_dir)
        sys.exit(1)

    session = Session(
        args.spec_dir,
        "settings.yml",
        output_root_dir=".moonleap/output",
    )
    session.load_settings()
    set_session(session)

    spec_fn = Path(args.spec_dir) / "spec.md"
    if not spec_fn.exists():
        report(f"Spec file not found: {spec_fn}")
        sys.exit(1)

    if args.action == "gen":
        generate_code(spec_fn, session)
        create_expected_dir(session.expected_dir, session.settings["references"])

    if args.action == "diff":
        if args.smart:
            create_symlinks(session)
        diff(session, args.sudo)
