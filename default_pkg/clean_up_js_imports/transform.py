import os
import re

import ramda as R
from moonleap.utils.fp import uniq
from parsimonious import Grammar, NodeVisitor

clean_up_js_imports_tag = "{% clean_up_js_imports %}"
end_clean_up_js_imports_tag = "{% end_clean_up_js_imports %}"


def parse_imports(text):
    grammar = Grammar(
        r"""
      imports         = (ws import ws)*
      import          = "import" ws (bracketed / star / singleton) ws "from" ws location
      singleton       = term ""
      bracketed       = "{" ws packages ws "}"
      star            = "*" ws "as" ws term
      packages        = (package ws "," ws packages) / package
      package         = term (ws "as" ws term)?
      term            = ~r"[a-zA-Z_0-9]+"
      location        = "'" ~r"[*a-zA-Z_\-\.0-9/]+" "'" ";"?
      ws              = ~r"\s*"
      """
    )

    class Visitor(NodeVisitor):
        def __init__(self):
            self.imports = {}
            self.clear()

        def clear(self):
            self.location = ""
            self.star = []
            self.packages = []
            self.singleton = []
            self.term = None

        def visit_star(self, node, visited_children):
            self.star.append(self.term)

        def visit_singleton(self, node, visited_children):
            self.singleton.append(node.text)

        def visit_package(self, node, visited_children):
            self.packages.append(node.text)

        def visit_term(self, node, visited_children):
            self.term = node.text

        def visit_location(self, node, visited_children):
            location = node.text

            if not location.endswith(";"):
                location += ";"

            record = self.imports.setdefault(
                location,
                {"location": location, "packages": [], "star": [], "singleton": []},
            )
            record["packages"].extend(self.packages)
            record["star"].extend(self.star)
            record["singleton"].extend(self.singleton)
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


def filter_packages(record, other_text):
    record["packages"] = sorted(
        uniq([x for x in record["packages"] if has_symbol(x, other_text)])
    )
    record["star"] = sorted([x for x in record["star"] if has_symbol(x, other_text)])
    record["singleton"] = sorted(
        [x for x in record["singleton"] if has_symbol(x, other_text)]
    )


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
        elif line == end_clean_up_js_imports_tag:
            count -= 1
            removing = False
            block_text = os.linesep.join(block)
            for location, record in sorted(
                parse_imports(block_text).items(), key=lambda x: x[0]
            ):
                filter_packages(record, other_text)
                for star in record["star"]:
                    result.extend([f"import * as {star} from {location}"])

                for singleton in record["singleton"]:
                    result.extend([f"import {singleton} from {location}"])

                if record["packages"]:
                    package_list = ", ".join(record["packages"])
                    result.extend([f"import {{ {package_list} }} from {location}"])
        elif removing:
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
        import { forEach } from 'ramda';
        import * as initiativesApi from 'src/initiatives/api';
    """
    )
    print(x)
