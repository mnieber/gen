import os

from moonleap.render.process_lines import process_lines


def p_section_callbacks(self, bvrs):
    facet_names = [x.name for x in bvrs]
    return process_lines(
        {
            101: r"setCallbacks(ctr.highlight, {",
            102: r"  highlightItem: {",
            103: r"    enter(this: HighlightCbs['highlightItem']) {",
            104: r"      FacetPolicies.cancelNewItemOnHighlightChange(ctr.highlight, this.id);",  # noqa
            105: r"    },",
            106: r"  },",
            107: r"} as HighlightCbs);",
        },
        remove={(102, 106): "addition" not in facet_names},
        indent=4,
    )


def p_section_policies(self, bvrs):
    indent = "      "
    result = [
        r"// highlight",
        r"Facets.highlightUsesItemLookUpTable(getm(Outputs_itemById)),",
    ]
    return os.linesep.join([(indent + x) for x in result])


def p_section_default_props(self, store):
    indent = "      "
    result = [
        f"{self.items_name}Highlight: () => state.{self.items_name}.highlight,",
        f"{self.item_name}: () => state.{self.items_name}.highlight.item,",
    ]
    return os.linesep.join([(indent + x) for x in result]) + os.linesep
