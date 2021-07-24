import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import ramda as R
from plumbum import local

from moonleap import (create_resources, get_blocks, render_resources,
                      report_resources)
from moonleap.report.create_expected_dir import create_expected_dir
from moonleap.session import Session, set_session


def generate_code(spec_file, session):
    blocks = get_blocks(spec_file)

    unmatched_rels = create_resources(blocks)
    render_resources(blocks, session)
    report_resources(blocks, session, unmatched_rels)


def diff(session):
    expected_dir = ".moonleap/expected"
    create_expected_dir(expected_dir, session.settings["references"])
    diff_tool = R.path_or("diff", ["bin", "diff_tool"])(session.settings)
    if diff_tool == "meld":
        local["meld"](".moonleap/output", expected_dir)
    else:
        report(f"Unknown diff tool: {diff_tool}")


def report(x):
    print(x)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--spec", required=True, dest="spec_dir")
    parser.add_argument("action", choices=["gen", "diff", "snap"])
    args = parser.parse_args()

    if not os.path.exists(args.spec_dir):
        report("Spec directory not found: " + args.spec_dir)
        sys.exit(1)

    session = Session(
        args.spec_dir,
        "settings.yml",
        output_root_dir=".moonleap/output",
    )
    session.load_settings()
    session.import_packages()
    set_session(session)

    spec_fn = Path(args.spec_dir) / "spec.md"
    if args.action == "gen":
        generate_code(spec_fn, session)

    if args.action == "diff":
        diff(session)
