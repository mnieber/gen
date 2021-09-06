import os
import sys
import traceback
from argparse import ArgumentParser
from pathlib import Path

from moonleap import create_resources, get_blocks, render_resources, report_resources
from moonleap.parser.expand_markdown import expand_markdown
from moonleap.render.file_writer import FileWriter
from moonleap.render.post_process_output_files import post_process_output_files
from moonleap.report.create_expected_dir import create_expected_dir
from moonleap.report.diff import create_symlinks, diff
from moonleap.session import Session, set_session


def create_parser():
    parser = ArgumentParser()
    parser.add_argument("--spec", required=True, dest="spec_dir")
    parser.add_argument(
        "--smart",
        required=False,
        action="store_true",
        help="If true, CRCs of output files are recorded, "
        + "and - on subsequent runs - output files are not written if "
        + "they have the same CRC. Moreover, output files are replaced with "
        + " a symlink if they have the same timestamp as the reference file.",
    )
    parser.add_argument(
        "--restore-missing",
        required=False,
        action="store_true",
        dest="restore_missing_files",
        help="If true, missing output files are recreated when using --smart mode",
    )
    parser.add_argument("--output-dir", required=False, default=".moonleap")
    parser.add_argument("--sudo", required=False, action="store_true")
    parser.add_argument("--stacktrace", required=False, action="store_true")
    parser.add_argument("action", choices=["gen", "diff"])

    return parser


def _create_file_writer(args):
    file_writer = FileWriter(
        session.snapshot_fn,
        check_crc_before_write=args.smart,
        restore_missing_files=args.restore_missing_files,
    )
    return file_writer


def generate_code(spec_file, session, file_writer):
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
    render_resources(blocks, file_writer.write_file)
    file_writer.write_merged_files_and_snapshot()
    for warning in file_writer.warnings:
        session.report(warning)

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
    parser = create_parser()
    args = parser.parse_args()

    if args.smart and args.action != "gen":
        raise Exception("You can only use --smart with the 'gen' action")

    if args.restore_missing_files and not args.smart:
        raise Exception("You can only use --restore-missing together with --smart")

    if args.sudo and args.action != "diff":
        raise Exception("You can only use --sudo with the 'diff' action")

    if not os.path.exists(args.spec_dir):
        report("Spec directory not found: " + args.spec_dir)
        sys.exit(1)

    session = Session(
        args.spec_dir,
        "settings.yml",
        output_root_dir=args.output_dir,
    )
    session.load_settings()
    set_session(session)

    spec_fn = Path(args.spec_dir) / "spec.md"
    if not spec_fn.exists():
        report(f"Spec file not found: {spec_fn}")
        sys.exit(1)

    if args.action == "gen":
        try:
            if args.smart:
                create_symlinks(session)
            generate_code(spec_fn, session, _create_file_writer(args))
            create_expected_dir(session.expected_dir, session.settings["references"])
        except Exception as e:
            report("Error: " + str(e))
            if args.stacktrace:
                traceback.print_exc()
        finally:
            pass

    if args.action == "diff":
        diff(session, args.sudo)
