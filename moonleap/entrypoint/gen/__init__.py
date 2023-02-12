from moonleap.report.create_expected_dir import create_expected_dir
from moonleap.report.symlinks import (
    create_symlinks_for_identical_files,
    create_symlinks_for_skip_patterns,
)

from .create_file_writer import create_file_writer
from .generate_code import generate_code


def gen(args, smart, session):
    create_expected_dir(session.expected_dir, session.settings["references"])

    if smart:
        if not args.no_scan:
            create_symlinks_for_identical_files(session)
            create_symlinks_for_skip_patterns(session)

    generate_code(
        session, create_file_writer(session, args), args.post_process_all_files
    )
