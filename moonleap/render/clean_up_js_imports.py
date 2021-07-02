import os
import re

import ramda as R
from parsimonious import Grammar, NodeVisitor

clean_up_js_imports_tag = "{% clean_up_js_imports %}"
end_clean_up_js_imports_tag = "{% end_clean_up_js_imports %}"


def parse_imports(text):
    grammar = Grammar(
        r"""
      imports         = ws import* ws
      import          = "import " something " from " location ws
      something       = (thing ", " something) / thing
      thing           = bracketed_atoms / atom
      bracketed_atoms = "{ " atoms " }"
      atoms           = (atom ", " atoms) / atom
      atom            = term (" as " term)?
      term            = ~r"[*a-zA-Z_0-9]+"
      location        = "'" ~r"[*a-zA-Z_\-\.0-9/]+" "';"
      ws              = ~r"\s*"
      """
    )

    class Visitor(NodeVisitor):
        def __init__(self):
            self.imports = {}
            self.clear()

        def clear(self):
            self.location = ""
            self.bare_atoms = []
            self.bracketed_atoms = []
            self.atoms = []

        def visit_thing(self, node, visited_children):
            if len(node.children) == 1:
                self.bare_atoms.extend(self.atoms)
            else:
                self.bracketed_atoms.extend(self.atoms)

        def visit_atom(self, node, visited_children):
            self.atoms.append(node.text)

        def visit_location(self, node, visited_children):
            location = node.text
            record = self.imports.setdefault(
                location,
                {"location": location, "bare_atoms": [], "bracketed_atoms": []},
            )
            record["bare_atoms"].extend(self.bare_atoms)
            record["bracketed_atoms"].extend(self.bracketed_atoms)
            self.clear()

        def generic_visit(self, node, visited_children):
            return visited_children or node

    tree = grammar.parse(text)
    visitor = Visitor()
    visitor.visit(tree)

    return visitor.imports


def process_clean_up_js_imports(lines):
    def t(x):
        has_tag = x == clean_up_js_imports_tag or x == end_clean_up_js_imports_tag

        return ("{% raw %}" + x + "{% endraw %}" + os.linesep) if has_tag else x

    return R.map(t, lines)


def get_other_text(lines):
    result = []
    removing = False

    for line in lines:
        if line == clean_up_js_imports_tag:
            removing = True
        elif line == end_clean_up_js_imports_tag:
            removing = False
        elif not removing:
            result.append(line)

    return os.linesep.join(result)


def has_symbol(x, text):
    parts = x.split()
    if len(parts) == 3 and parts[1] == "as":
        symbol = parts[2]
    elif len(parts) == 1:
        symbol = x
    else:
        raise Exception("Expected import to be either <x> or <x> as <y>")
    return re.search(r"\b" + symbol + r"\b", text)


def filter_atoms(record, other_text):
    record["bare_atoms"] = [
        x for x in record["bare_atoms"] if has_symbol(x, other_text)
    ]
    record["bracketed_atoms"] = [
        x for x in record["bracketed_atoms"] if x in other_text
    ]


def post_process_clean_up_js_imports(lines):
    result = []
    removing = False
    block = []
    count = 0
    other_text = get_other_text(lines)

    for line in lines:
        if line == clean_up_js_imports_tag:
            count += 1
            removing = True
            block.clear()
            continue

        if line == end_clean_up_js_imports_tag:
            count -= 1
            removing = False
            block_text = os.linesep.join(block)
            for location, record in parse_imports(block_text).items():
                filter_atoms(record, other_text)
                if record["bare_atoms"] or record["bracketed_atoms"]:
                    bare_atoms = ", ".join(record["bare_atoms"])
                    bracketed_atoms = ", ".join(record["bracketed_atoms"])
                    infix = ", " if bare_atoms and bracketed_atoms else ""
                    result.extend(
                        [
                            f"import {{ {bare_atoms + infix + bracketed_atoms} }} from {location}"
                        ]
                    )
            continue

        if removing:
            block.append(line)
        else:
            result.append(line)

    if count != 0:
        raise Exception(
            "{% clean_up_js_imports %} not matched equally by "
            + "{% end_clean_up_js_imports %}"
        )

    return result


if __name__ == "__main__":
    x = parse_imports(
        """
        import { makeObservable } from 'mobx';

        import { action, observable, makeObservable } from 'mobx';
        import { RST, resetRS, updateRes } from 'src/utils/RST';
        import { forEach } from 'lodash/fp';
        import * as initiativesApi from 'src/initiatives/api';
    """
    )
    print(x)
