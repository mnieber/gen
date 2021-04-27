import os

from moonleap.render.process_lines import process_lines


def callbacks_section(self):
    facet_names = [x.name for x in self.container.behaviors]
    return process_lines(
        {
            101: r"setCallbacks(this.highlight, {",
            102: r"  highlightItem: {",
            103: r"    enter(this: HighlightCbs['highlightItem']) {",
            104: r"      FacetPolicies.cancelNewItemOnHighlightChange(ctr.highlight, this.id);",
            105: r"    },",
            106: r"  },",
            107: r"} as HighlightCbs);",
        },
        remove={(102, 106): "addition" not in facet_names},
        indent=4,
    )


def policies_section(self):
    indent = "        "
    result = [
        r"// highlight",
        r"Facets.highlightUsesItemLookUpTable(getm(Outputs_itemById)),",
    ]
    return os.linesep.join([(indent + x) for x in result])
