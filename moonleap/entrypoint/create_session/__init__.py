import os

from moonleap.packages.scope_manager import ScopeManager
from moonleap.render.file_writer import FileWriter
from moonleap.session import Session, set_session


def create_session(args):
    if not os.path.exists(args.spec_dir):
        raise Exception("Spec directory not found: " + args.spec_dir)

    session = Session(
        args.spec_dir,
        "settings.yml",
        output_root_dir=args.output_dir,
    )
    set_session(session)
    session.init(
        ScopeManager(),
        FileWriter(
            session.snapshot_fn,
            check_crc_before_write=args.smart,
        ),
    )
    session.load_settings()
    return session
