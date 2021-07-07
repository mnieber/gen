import os
from collections import defaultdict

from moonleap import Term, upper0
from moonleap.utils.inflect import plural


def bvrs_by_item_name(self):
    result = defaultdict(lambda: [])
    for bvr in self.behaviors:
        result[self.item_name].append(bvr)
    for item_list in self.item_lists:
        result.setdefault(item_list.item_name, [])
    return result


def store_by_item_name(self):
    result = {}
    stores = []
    for x in self.module.service.modules:
        stores.extend(x.stores)

    for item_name in bvrs_by_item_name(self).keys():
        for store in stores:
            if [x for x in store.item_lists if x.item_name == item_name]:
                result[item_name] = store
                break
    return result


def constructor_section(self):
    indent = "  "
    result = []

    for item_name, bvrs in self.bvrs_by_item_name.items():
        result += [f"{plural(item_name)} = {{"]
        for bvr in bvrs:
            result += [bvr.constructor_section]
        result += [r"};"]

    return os.linesep.join([(indent + x) for x in result])


def callbacks_section(self):
    indent = "  "
    result = []

    for item_name, bvrs in self.bvrs_by_item_name.items():
        redRoses = plural(item_name)

        body = []
        for bvr in bvrs:
            body += [bvr.callbacks_section(self.behaviors)]

        result += [f"_set{upper0(redRoses)}Callbacks(props: PropsT) {{"]

        if body:
            result += [
                f"  const ctr = this.{redRoses};",
                #
                *body,
            ]

        result += [r"}", ""]

    return os.linesep.join([(indent + x) for x in result])


def declare_policies_section(self, item_name):
    indent = "    "
    result = [
        f"const Inputs_items = [Inputs, '{plural(item_name)}', this] as CMT;",
        f"const Outputs_display = [Outputs, '{plural(item_name)}Display', this] as CMT;",
    ]

    return os.linesep.join([(indent + x) for x in result])


def policies_section(self):
    facet_names = [x.name for x in self.behaviors]
    indent = "      "
    result = []

    if "filtering" not in facet_names:
        result += [
            r"Skandha.mapDataToFacet(Outputs_display, getm(Inputs_items)),",
        ]

    return os.linesep.join([(indent + x) for x in result])


def type_import_path(self, type_name):
    for module in self.module.service.modules:
        for store in module.stores:
            if [x for x in store.item_types if x.name == type_name]:
                return f"{store.module_path}/types"
    return None
