from moonleap.report.create_expected_dir import create_expected_dir

from .generate_code import generate_code


def gen(args, smart, session):
    create_expected_dir(session.expected_dir, session.settings["references"])
    generate_code(session, args.post_process_all_files)
