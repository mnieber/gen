_session = None


class Session:
    def __init__(self, settings, output_root_dir):
        self.settings = settings
        self.output_root_dir = output_root_dir
        self.unmatched_rels = []

    def report(self, x):
        print(x)


def set_session(session):
    global _session

    if _session:
        raise Exception("There already is a session")
    _session = session


def get_session():
    if not _session:
        raise Exception("There is no session")
    return _session
