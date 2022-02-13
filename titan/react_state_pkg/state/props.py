import os

from moonleap import u0
from moonleap.utils.inflect import plural


def has_bvrs(self):
    return [p for p in self.pipelines if p.bvrs]


def get_context(state):
    _ = lambda: None
    _.pipelines = [p for p in state.pipelines if p.bvrs]

    bvr_names = set()
    _.bvrs = list()
    for pipeline in _.pipelines:
        for bvr in pipeline.bvrs:
            if bvr.name not in bvr_names:
                bvr_names.add(bvr.name)
                _.bvrs.append(bvr)

    class Sections:
        def constructor(self):
            indent = "  "
            result = []

            for pipeline in _.pipelines:
                result += [f"{plural(pipeline.output.item_name)} = {{"]
                for bvr in pipeline.bvrs:
                    result += [bvr.sections.constructor()]
                result += [r"};"]

            return os.linesep.join([(indent + x) for x in result])

        def callbacks(self):
            indent = "  "
            result = []

            for pipeline in _.pipelines:
                items_name = plural(pipeline.output.item_name)

                body = []
                for bvr in pipeline.bvrs:
                    body += [bvr.sections.callbacks(pipeline.bvrs)]

                result += [f"_set{u0(items_name)}Callbacks(props: PropsT) {{"]

                if body:
                    result += [f"  const ctr = this.{items_name};"]
                    result += body

                result += [r"}", ""]

            return os.linesep.join([(indent + x) for x in result])

        def policies(self, pipeline):
            indent = "      "
            result = []

            if not pipeline.get_bvr("filtering"):
                result += [
                    r"Skandha.mapDataToFacet(Outputs_display, getm(Inputs_items)),",
                ]

            return os.linesep.join([(indent + x) for x in result])

    return dict(sections=Sections(), _=_)
