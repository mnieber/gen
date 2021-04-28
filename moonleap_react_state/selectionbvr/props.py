import os

from moonleap.render.process_lines import process_lines


def imports_section(self):
    return (
        "import { Selection, SelectionCbs, handleSelectItem } "
        + "from 'skandha-facets/Selection'"
    )


def callbacks_section(self):
    facet_names = [x.name for x in self.state.behaviors]
    return process_lines(
        {
            101: r"setCallbacks(ctr.selection, {{",
            102: r"  selectItem: {",
            103: r"    selectItem(this: SelectionCbs['selectItem']) {",
            104: r"      handleSelectItem(ctr.selection, this.selectionParams);",
            105: r"      FacetPolicies.highlightFollowsSelection(",
            106: r"        ctr.selection,",
            107: r"        this.selectionParams",
            108: r"      );",
            109: r"    }",
            110: r"  },",
            111: r"} as SelectionCbs);",
        },
        remove={(105, 108): "highlight" not in facet_names},
        indent=4,
    )


def declare_policies_section(self):
    indent = "    "
    result = [
        f"const Outputs_itemById = [Outputs, '{self.item_name}ById', this] as CMT;",
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
