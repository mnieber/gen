import os
from collections import defaultdict

from moonleap import Term
from moonleap.utils.inflect import plural


def bvrs_by_item_name(self):
    result = defaultdict(lambda: [])
    for bvr in self.behaviors:
        item_name = bvr.item_name or self.item_name
        result[item_name].append(bvr)
    return result


def constructor_section(self):
    indent = "  "
    result = [
        f"inputs = new Inputs();",
        f"outputs = new Outputs();",
    ]

    return os.linesep.join([(indent + x) for x in result])


def declare_policies_section(self, item_name):
    facet_names = [x.name for x in self.behaviors]
    indent = "    "
    result = [
        f"const Inputs_items = [Inputs, '{plural(item_name)}', this] as CMT;",
    ]
    if "filtering" not in facet_names:
        result += [
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
            return resource.import_path
    return None
