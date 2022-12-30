import os
import re


def _find_include_snippet_statement(text):
    regex = r"{% include_snippet [\"\'](?P<fn>[A-Za-z0-9_/\-\.\|]+)[\"\'](?P<maybe> maybe=True)? %}"
    matches = list(re.finditer(regex, text, re.MULTILINE))
    if matches:
        maybe = matches[0].group("maybe")
        return matches[0].group("fn"), maybe
    return None


def process_include_snippets(lines, template_fn):
    result = []
    for block_line in lines:
        snippet_match = _find_include_snippet_statement(block_line)

        if snippet_match:
            snippet_fn, maybe = snippet_match
            fn = os.path.join(os.path.dirname(template_fn), snippet_fn)
            if os.path.exists(fn):
                with open(fn) as f:
                    result.extend(f.readlines())
            elif not maybe:
                raise Exception(f"Snippet file not found: {fn}")
        else:
            result.append(block_line)

    return result
