def get_helpers(_):
    class Helpers:
        state = _.component
        pipelines = [p for p in state.pipelines if p.bvrs]
        bvrs = list()

        def __init__(self):
            bvr_names = set()
            for pipeline in self.pipelines:
                for bvr in pipeline.bvrs:
                    if bvr.name not in bvr_names:
                        bvr_names.add(bvr.name)
                        self.bvrs.append(bvr)

        def has_bvr(self, name):
            return [x for x in self.bvrs if x.name == name]

    return Helpers()
