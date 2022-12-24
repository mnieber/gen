from moonleap.session import Session, set_session


def create_session(args):
    session = Session(
        args.spec_dir,
        "settings.yml",
        output_root_dir=args.output_dir,
    )
    session.load_settings()
    set_session(session)
    return session
