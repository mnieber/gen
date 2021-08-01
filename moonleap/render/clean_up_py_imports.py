import os
import re

import ramda as R
from parsimonious import Grammar, NodeVisitor

clean_up_py_imports_tag = "{% clean_up_py_imports %}"
end_clean_up_py_imports_tag = "{% end_clean_up_py_imports %}"


def parse_imports(text):
    grammar = Grammar(
        r"""
      statement       = (ws (import_from_loc / import) ws)*
      import          = "import" ws modules
      import_from_loc = "from" ws location ws "import" ws modules
      modules         = (module ws "," ws modules) / module
      module          = term (ws "as" ws term)?
      location        = term ""
      term            = ~r"[\.a-zA-Z_0-9]+"
      ws              = ~r"\s*"
      """
    )

    class Visitor(NodeVisitor):
        def __init__(self):
            self.imports = {}
            self.clear()

        def clear(self):
            self.location = ""
            self.modules = []
            self.location = None

        def visit_module(self, node, visited_children):
            self.modules.append(node.text)

        def visit_location(self, node, visited_children):
            self.location = node.text

        def visit_import_from_loc(self, node, visited_children):
            record = self.imports.setdefault(
                self.location,
                {"location": self.location, "modules": []},
            )
            record["modules"].extend(self.modules)
            self.clear()

        def visit_import(self, node, visited_children):
            record = self.imports.setdefault(
                "import",
                {"location": None, "modules": []},
            )
            record["modules"].extend(self.modules)
            self.clear()

        def generic_visit(self, node, visited_children):
            return visited_children or node

    tree = grammar.parse(text)
    visitor = Visitor()
    visitor.visit(tree)

    return visitor.imports


def process_clean_up_py_imports(lines):
    def t(x):
        has_tag = x == clean_up_py_imports_tag or x == end_clean_up_py_imports_tag

        return ("{% raw %}" + x + "{% endraw %}" + os.linesep) if has_tag else x

    return R.map(t, lines)


def get_other_text(lines):
    result = []
    removing = False

    for line in lines:
        if line == clean_up_py_imports_tag:
            removing = True
        elif line == end_clean_up_py_imports_tag:
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


def filter_modules(record, other_text):
    record["modules"] = R.uniq(
        [x for x in record["modules"] if has_symbol(x, other_text)]
    )


def post_process_clean_up_py_imports(lines):
    result = []
    removing = False
    block = []
    count = 0
    other_text = get_other_text(lines)

    for line in lines:
        if line == clean_up_py_imports_tag:
            count += 1
            removing = True
            block.clear()
        elif line == end_clean_up_py_imports_tag:
            count -= 1
            removing = False
            block_text = os.linesep.join(block)
            for location, record in parse_imports(block_text).items():
                filter_modules(record, other_text)
                if record["modules"]:
                    location = record["location"]
                    if location:
                        module_list = ", ".join(record["modules"])
                        result.extend([f"from {location} import {module_list}"])
                    else:
                        for module in record["modules"]:
                            result.extend([f"import {module}"])
        elif removing:
            block.append(line)
        else:
            result.append(line)

    if count != 0:
        raise Exception(
            "{% clean_up_py_imports %} not matched equally by "
            + "{% end_clean_up_py_imports %}"
        )

    return result


if __name__ == "__main__":
    x = parse_imports(
        """
        from dataclasses import field, bar as hello, baz
        import sys
        import os.path as foo, dataclasses
    """
    )
    print(x)
