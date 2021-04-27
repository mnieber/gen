import os


def declare_policies_section(self):
    facet_names = [x.name for x in self.behaviors]
    indent = "      "
    result = [
        f"const Inputs_items = [Inputs, 'items'] as CMT;",
    ]
    if "filtering" not in facet_names:
        result += [
            r"const Outputs_display = [Outputs, 'display'] as CMT;",
        ]

    return os.linesep.join([(indent + x) for x in result])


def policies_section(self):
    facet_names = [x.name for x in self.behaviors]
    indent = "        "
    result = []

    if "filtering" not in facet_names:
        result += [
            r"mapDataToFacet(Outputs_display, getm(Inputs_items)),",
        ]

    return os.linesep.join([(indent + x) for x in result])
