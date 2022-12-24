from moonleap.entrypoint.create_file_writer import create_file_writer
from moonleap.entrypoint.generate_code import generate_code
from moonleap.report.create_expected_dir import create_expected_dir
from moonleap.report.symlinks import (
    create_symlinks_for_identical_files,
    create_symlinks_for_skip_patterns,
)


def gen(args, smart, session, spec_fn):
    create_expected_dir(session.expected_dir, session.settings["references"])

    if smart:
        create_symlinks_for_identical_files(session)
    if args.smart_with_skip:
        create_symlinks_for_skip_patterns(session)

    generate_code(
        spec_fn,
        session,
        create_file_writer(session, args),
        args.post_process_all_files,
    )
