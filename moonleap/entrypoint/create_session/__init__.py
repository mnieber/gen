import os
from pathlib import Path

from moonleap.session import Session, set_session
from moonleap.session.workspace import Workspace


def create_session(args):
    if not os.path.exists(args.spec_dir):
        raise Exception("Spec directory not found: " + args.spec_dir)

    session = Session()
    set_session(session)
    session.load_settings(Path(args.spec_dir) / "settings.yml")

    workspace = Workspace(spec_dir=args.spec_dir, output_root_dir=args.output_dir)
    workspace.init(is_smart=args.smart)
    session.init(workspace)

    return session
