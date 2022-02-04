import bisect
import os

import ramda as R
from moonleap import u0
from moonleap.utils.inflect import plural
from titan.react_pkg.pkg.ml_get import ml_react_app


def _find_module_that_provides_item_list(react_app, item_name):
    for module in react_app.modules:
        for state in module.states:
            for item_list in state.item_lists_provided:
                if item_list.item_name == item_name:
                    return module
    return None


def bvrs_by_item_name(self):
    result = dict()
    for bvr in self.behaviors:
        bvrs = result.setdefault(bvr.item_name, [])
        pos = bisect.bisect_left(R.map(R.prop("name"))(bvrs), bvr.name)
        result[bvr.item_name].insert(pos, bvr)
    for item_list in self.item_lists_provided:
        result.setdefault(item_list.item_name, [])
    return result


def type_import_path(self, item_name):
    module = _find_module_that_provides_item_list(ml_react_app(self), item_name)
    if module:
        return f"{module.module_path}/types"
    return None


def get_context(state):
    _ = lambda: None
    _.facet_names_by_item_name = dict()
    for item_name, bvrs in state.bvrs_by_item_name.items():
        _.facet_names_by_item_name[item_name] = [x.name for x in bvrs]

    class Sections:
        def constructor(self):
            indent = "  "
            result = []

            for item_name, bvrs in state.bvrs_by_item_name.items():
                result += [f"{plural(item_name)} = {{"]
                for bvr in bvrs:
                    result += [bvr.sections.constructor()]
                result += [r"};"]

            return os.linesep.join([(indent + x) for x in result])

        def callbacks(self):
            indent = "  "
            result = []

            for item_name, bvrs in state.bvrs_by_item_name.items():
                redRoses = plural(item_name)

                body = []
                for bvr in bvrs:
                    body += [bvr.sections.callbacks(state.behaviors)]

                result += [f"_set{u0(redRoses)}Callbacks(props: PropsT) {{"]

                if body:
                    result += [f"  const ctr = this.{redRoses};"]
                    result += body

                result += [r"}", ""]

            return os.linesep.join([(indent + x) for x in result])

        def policies(self, item_name):
            indent = "      "
            result = []

            if "filtering" not in _.facet_names_by_item_name[item_name]:
                result += [
                    r"Skandha.mapDataToFacet(Outputs_display, getm(Inputs_items)),",
                ]

            return os.linesep.join([(indent + x) for x in result])

    return dict(sections=Sections(), _=_)
