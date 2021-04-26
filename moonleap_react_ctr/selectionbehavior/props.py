import os


def imports_section(self):
    return (
        "import { Selection, SelectionCbs, handleSelectItem } "
        + "from 'skandha-facets/Selection'"
    )


def callbacks_section(self):
    facet_names = [x.name for x in self.container.behaviors]
    indent = "    "
    result = []

    if True:
        result += [
            f"setCallbacks(this.{self.name}, {{",
            r"  selectItem: {",
            r"    selectItem(this: SelectionCbs['selectItem']) {",
            r"      handleSelectItem(ctr.selection, this.selectionParams);",
        ]

    if "highlight" in facet_names:
        result += [
            r"      FacetPolicies.highlightFollowsSelection(",
            r"        ctr.selection,",
            r"        this.selectionParams",
            r"      );",
        ]

    if True:
        result += [
            r"    };",
            r"  },",
            r"} as SelectionCbs);",
        ]

    return os.linesep.join([(indent + x) for x in result])


def declare_policies_section(self):
    indent = "      "
    result = [
        f"const Outputs_itemById = [Outputs, '{self.container.item_name}ById'] as CMT;",
        f"const Outputs_display = [Outputs, 'display'] as CMT;",
    ]
    return os.linesep.join([(indent + x) for x in result])


def policies_section(self):
    indent = "      "
    result = [
        r"// selection",
        r"Facets.selectionUsesSelectableIds(getm(Outputs_display), getIds),",
        r"Facets.selectionUsesItemLookUpTable(getm(Outputs_itemById)),",
    ]
    return os.linesep.join([(indent + x) for x in result])
