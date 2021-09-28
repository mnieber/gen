import bisect
import os

import ramda as R
from moonleap import u0
from moonleap.utils.inflect import plural
from titan.react_pkg.reactapp.resources import find_module_that_provides_item_list


def bvrs_by_item_name(self):
    result = dict()
    for bvr in self.behaviors:
        bvrs = result.setdefault(bvr.item_name, [])
        pos = bisect.bisect_left(R.map(R.prop("name"))(bvrs), bvr.name)
        result[bvr.item_name].insert(pos, bvr)
    for item_list in self.item_lists:
        result.setdefault(item_list.item_name, [])
    return result


def store_by_item_name(self):
    result = {}
    stores = []
    for x in self.module.react_app.modules:
        stores.extend(x.stores)

    for item_name in bvrs_by_item_name(self).keys():
        for store in stores:
            if [x for x in store.item_lists if x.item_name == item_name]:
                result[item_name] = store
                break
    return result


def type_import_path(self, type_name):
    module = find_module_that_provides_item_list(self.module.react_app, type_name)
    if module:
        return f"{module.module_path}/types"
    return None


class Sections:
    def __init__(self, res):
        self.res = res

    def constructor(self):
        indent = "  "
        result = []

        for item_name, bvrs in self.res.bvrs_by_item_name.items():
            result += [f"{plural(item_name)} = {{"]
            for bvr in bvrs:
                result += [bvr.sections.constructor()]
            result += [r"};"]

        return os.linesep.join([(indent + x) for x in result])

    def callbacks(self):
        indent = "  "
        result = []

        for item_name, bvrs in self.res.bvrs_by_item_name.items():
            redRoses = plural(item_name)

            body = []
            for bvr in bvrs:
                body += [bvr.sections.callbacks(self.res.behaviors)]

            result += [f"_set{u0(redRoses)}Callbacks(props: PropsT) {{"]

            if body:
                result += [
                    f"  const ctr = this.{redRoses};",
                    #
                    *body,
                ]

            result += [r"}", ""]

        return os.linesep.join([(indent + x) for x in result])

    def declare_policies(self, item_name):
        indent = "    "
        items = plural(item_name)
        result = [
            f"const Inputs_items = [Inputs, '{items}', this] as CMT;",
            f"const Outputs_display = [Outputs, '{items}Display', this] as CMT;",  # noqa: E501
        ]

        return os.linesep.join([(indent + x) for x in result])

    def policies(self):
        facet_names = [x.name for x in self.res.behaviors]
        indent = "      "
        result = []

        if "filtering" not in facet_names:
            result += [
                r"Skandha.mapDataToFacet(Outputs_display, getm(Inputs_items)),",
            ]

        return os.linesep.join([(indent + x) for x in result])


def get_context(self):
    return dict(sections=Sections(self))
