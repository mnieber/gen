from .check_args import check_args  # noqa: F401
from .create_output_dir import create_output_dir
from .generate_code import generate_code
from .parse_args import parse_args  # noqa: F401


def gen(args, session):
    create_output_dir(session.ws.output_dir, session.get_setting_or({}, ["references"]))
    generate_code(session)
