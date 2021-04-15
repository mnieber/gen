import os


def import_path(self):
    return os.path.join(self.store.module.output_path, "types")
