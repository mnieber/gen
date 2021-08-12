import os


def module_path(self):
    return os.path.join(self.store.module.output_path)
