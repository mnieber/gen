def module_path(self):
    return self.name


def get_module(self, module_name):
    for module in self.modules:
        if module.name == module_name:
            return module
    return None
