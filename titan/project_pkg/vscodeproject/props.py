from titan.project_pkg.vscodeproject.resources import VsCodeProjectConfig


def _merge(lhs, rhs):
    result = VsCodeProjectConfig()
    result.paths = lhs.paths + [x for x in rhs.paths if x not in lhs.paths]
    return result


def get_config(self):
    result = VsCodeProjectConfig()
    for config in self.vs_code_project_configs.merged:
        result = _merge(result, config)
    return result


def paths(self):
    return self.get_config().paths
