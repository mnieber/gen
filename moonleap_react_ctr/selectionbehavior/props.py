import os

from moonleap import upper0
from moonleap.utils.inflect import plural


def imports_section(self):
    return f"import {{ Selection, SelectionCbs, handleSelectItem }} from 'skandha-facets/Selection'"


def callbacks_section(self):
    facet_names = [x.name for x in self.container.behaviors]
    indent = "    "
    result = []

    if True:
        result += [
            f"setCallbacks(this.{self.name}, {{",
            f"  selectItem: {{",
            f"    selectItem(this: SelectionCbs['selectItem']) {{",
            f"      handleSelectItem(ctr.selection, this.selectionParams);",
        ]

    if "highlight" in facet_names:
        result += [
            f"      FacetPolicies.highlightFollowsSelection(",
            f"        ctr.selection,",
            f"        this.selectionParams",
            f"      );",
        ]

    if True:
        result += [
            f"    }};",
            f"  }},",
            f"}} as SelectionCbs);",
        ]

    return os.linesep.join([(indent + x) for x in result])


def declare_policies_section(self):
    indent = "      "
    result = [
        f"const Outputs_itemById = [Outputs, '{self.container.item_name}ById'] as CMT;",
        f"const Outputs_ids = [Outputs, '{self.container.item_name}Ids'] as CMT;",
    ]
    return os.linesep.join([(indent + x) for x in result])


def policies_section(self):
    indent = "      "
    result = [
        f"// selection",
        f"Facets.selectionUsesSelectableIds(getm(Outputs_ids)),",
        f"Facets.selectionUsesItemLookUpTable(getm(Outputs_itemById)),",
    ]
    return os.linesep.join([(indent + x) for x in result])
