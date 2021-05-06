import os
from collections import defaultdict

from moonleap import Term, upper0
from moonleap.utils.inflect import plural


def bvrs_by_item_name(self):
    result = defaultdict(lambda: [])
    for bvr in self.behaviors:
        item_name = bvr.item_name or self.item_name
        result[item_name].append(bvr)
    return result


def store_by_item_name(self):
    result = {}
    stores = [x.store for x in self.module.service.modules if x.store]

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
        result += [
            f"_set{upper0(redRoses)}Callbacks(props: PropsT) {{",
            f"  const ctr = this.{redRoses};",
        ]
        for bvr in bvrs:
            result += [bvr.callbacks_section(self.behaviors)]
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
            r"mapDataToFacet(Outputs_display, getm(Inputs_items)),",
        ]

    return os.linesep.join([(indent + x) for x in result])


def type_import_path(self, type_name):
    term = Term(type_name, "item-type")
    for parent_block in self.block.get_blocks(include_self=True, include_parents=True):
        resource = parent_block.get_resource(term)
        if resource:
            return resource.module_path + "/types"
    return None
