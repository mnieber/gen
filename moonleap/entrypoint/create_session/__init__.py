import os

from moonleap.session import Session, set_session


def create_session(args):
    if not os.path.exists(args.spec_dir):
        raise Exception("Spec directory not found: " + args.spec_dir)

    session = Session(
        args.spec_dir,
        "settings.yml",
        output_root_dir=args.output_dir,
    )
    session.load_settings()
    set_session(session)
    return session
