import os
import re


def _find_include_snippet_statement(text):
    regex = r"{% include_snippet [\"\'](?P<fn>[A-Za-z0-9_/\-\.\|]+)[\"\'] %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    return matches[0].group("fn") if matches else None


def process_include_snippets(lines, template_fn):
    result = []
    for block_line in lines:
        snippet_fn = _find_include_snippet_statement(block_line)

        if snippet_fn:
            fn = os.path.join(os.path.dirname(template_fn), snippet_fn)
            with open(fn) as f:
                result.extend(f.readlines())
        else:
            result.append(block_line)

    return result
