class Session:
    def __init__(self, settings, output_root_dir):
        self.settings = settings
        self.output_root_dir = output_root_dir
        self.unmatched_rels = []
