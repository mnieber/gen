import os

from moonleap.render.process_lines import process_lines
from titan.react_state_pkg.behavior.props import Sections as BehaviourSections


class Sections(BehaviourSections):
    def __init__(self, res):
        self.res = res

    def callbacks(self, bvrs):
        facet_names = [x.name for x in bvrs]
        return process_lines(
            {
                101: r"setCallbacks(ctr.highlight, {",
                102: r"  highlightItem: {",
                103: r"    enter(this: HighlightCbs['highlightItem']) {",
                104: r"      FacetPolicies.cancelNewItemOnHighlightChange(ctr.highlight, this.id);",  # noqa: E501
                105: r"    },",
                106: r"  },",
                107: r"} as HighlightCbs);",
            },
            remove={(102, 106): "addition" not in facet_names},
            indent=4,
        )

    def policies(self, bvrs):
        indent = "      "
        result = [
            r"// highlight",
            r"Facets.highlightUsesItemLookUpTable(getm(Outputs_itemById)),",
        ]
        return os.linesep.join([(indent + x) for x in result])

    def default_props(self, store):
        indent = "      "
        result = [
            f"{self.res.items_name}Highlight: () => state.{self.res.items_name}.highlight,",
            f"{self.res.item_name}: () => state.{self.res.items_name}.highlight.item,",
        ]
        return os.linesep.join([(indent + x) for x in result]) + os.linesep
