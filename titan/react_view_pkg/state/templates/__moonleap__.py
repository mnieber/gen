def get_helpers(_):
    class Helpers:
        containers = [p for p in _.state.containers if p.bvrs]
        bvrs = list()

        def __init__(self):
            bvr_names = set()
            for container in self.containers:
                for bvr in container.bvrs:
                    if bvr.name not in bvr_names:
                        bvr_names.add(bvr.name)
                        self.bvrs.append(bvr)

        def has_bvr(self, name):
            return [x for x in self.bvrs if x.name == name]

    return Helpers()
