import os

from moonleap import u0
from moonleap.render.process_lines import process_lines
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
        return process_lines(
            {
                101: r"setCallbacks(ctr.selection, {",
                102: r"  selectItem: {",
                103: r"    selectItem(this: SelectionCbs['selectItem']) {",
                104: r"      handleSelectItem(ctr.selection, this.selectionParams);",
                105: r"      FacetPolicies.highlightFollowsSelection(",
                106: r"        ctr.selection,",
                107: r"        this.selectionParams",
                108: r"      );",
                109: f"      props.navigateTo{u0(self.res.item_name)}(ctr.highlight.item);",
                110: r"    }",
                111: r"  },",
                112: r"} as SelectionCbs);",
            },
            remove={(105, 109): "highlight" not in facet_names},
            indent=4,
        )

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
