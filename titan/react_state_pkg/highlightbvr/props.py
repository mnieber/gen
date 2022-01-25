import os

from titan.react_state_pkg.behavior.props import Sections as BehaviourSections


class Sections(BehaviourSections):
    def __init__(self, res):
        self.res = res

    def callbacks(self, bvrs):
        facet_names = [x.name for x in bvrs]
        lines = [
            r"    setCallbacks(ctr.highlight, {",
            r"      highlightItem: {",
            r"        enter(this: HighlightCbs['highlightItem']) {",
            r"          FacetPolicies.cancelNewItemOnHighlightChange(ctr.highlight, this.id);",  # noqa: E501
            r"        },",
            r"      },",
            r"    } as HighlightCbs);",
        ]

        if "addition" not in facet_names:
            lines = lines[:1] + lines[6:]
        return os.linesep.join(lines)

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
            f"{self.res.items_name}Highlight: () => state.{self.res.items_name}.highlight,",  # noqa: E501
            f"{self.res.item_name}: () => state.{self.res.items_name}.highlight.item,",
        ]
        return os.linesep.join([(indent + x) for x in result]) + os.linesep
