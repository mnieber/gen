import os

from titan.react_state_pkg.behavior.props import Sections as BehaviourSections


class Sections(BehaviourSections):
    def __init__(self, res):
        self.res = res

    def imports(self):
        return (
            "import { Selection, SelectionCbs, handleSelectItem } "
            + "from 'skandha-facets/Selection';"
        )

    def callbacks(self, bvrs):
        facet_names = [x.name for x in bvrs]
        lines = [
            r"    setCallbacks(ctr.selection, {",
            r"      selectItem: {",
            r"        selectItem(this: SelectionCbs['selectItem']) {",
            r"          handleSelectItem(ctr.selection, this.selectionParams);",
            r"          FacetPolicies.highlightFollowsSelection(",
            r"            ctr.selection,",
            r"            this.selectionParams",
            r"          );",
            r"        }",
            r"      },",
            r"    } as SelectionCbs);",
        ]
        if "highlight" not in facet_names:
            lines = lines[:4] + lines[8:]
        return os.linesep.join(lines)

    def declare_policies(self, bvrs):
        indent = "    "
        result = [
            f"const Outputs_itemById = [Outputs, '{self.res.item_name}ById', this] as CMT;",  # noqa: E501
        ]
        return os.linesep.join([(indent + x) for x in result])

    def policies(self, bvrs):
        indent = "      "
        result = [
            r"// selection",
            r"Facets.selectionUsesSelectableIds(getm(Outputs_display), getIds),",
            r"Facets.selectionUsesItemLookUpTable(getm(Outputs_itemById)),",
        ]
        return os.linesep.join([(indent + x) for x in result])

    def default_props(self, store):
        indent = "      "
        result = [
            f"{self.res.items_name}Selection: () => state.{self.res.items_name}.selection,",  # noqa: E501
        ]
        return os.linesep.join([(indent + x) for x in result]) + os.linesep
