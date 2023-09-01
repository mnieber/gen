def get_helpers(_):
    class Helpers:
        containers = [p for p in _.state.containers]
        bvrs_to_import = list()
        other_bvrs = list()

        def __init__(self):
            bvr_names = set()
            for container in self.containers:
                for bvr in container.bvrs:
                    if bvr.is_skandha:
                        if bvr.name not in bvr_names:
                            bvr_names.add(bvr.name)
                            self.bvrs_to_import.append(bvr)
                    else:
                        self.other_bvrs.append(bvr)

        def import_bvr(self, name):
            return [x for x in self.bvrs_to_import if x.name == name]

    return Helpers()
