from .check_args import check_args  # noqa: F401
from .create_expected_dir import create_expected_dir
from .generate_code import generate_code
from .parse_args import parse_args  # noqa: F401


def gen(args, session):
    create_expected_dir(
        session.ws.expected_dir, session.get_setting_or({}, ["references"])
    )
    generate_code(session, args.post_process_all_files)
