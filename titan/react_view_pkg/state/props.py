from moonleap.utils.case import l0


def has_bvrs(self):
    return [p for p in self.pipelines if p.bvrs]


def state_ts_var(state):
    return l0(state.name)
