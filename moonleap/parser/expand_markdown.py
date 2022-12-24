import re
from pathlib import Path

import mistune


# The output_fn arg should be provided when you want to have a dump of the
# expanded markdown. This is useful for debugging.
def expand_markdown(spec_file, output_fn=None, base_level=0, scope_names=None):
    if scope_names is None:
        scope_names = []

    parse_fn = _get_one_time_parse_fn(spec_file, base_level, scope_names)
    expanded_markdown = parse_fn(_get_raw_markdown(spec_file))
    if output_fn:
        _write_expanded_markdown(output_fn, expanded_markdown)

    return expanded_markdown


def _get_one_time_parse_fn(spec_file, base_level, scope_names):
    from moonleap.parser.block_expander import BlockExpander

    expander = BlockExpander(Path(spec_file).parent, base_level, scope_names)
    parser = CustomMarkdown(renderer=expander)
    called = False

    def f(raw_markdown):
        nonlocal called
        if called:
            raise Exception("This function may be called only once")
        called = True
        parser(raw_markdown)
        return expander.output_text

    return f


def _write_expanded_markdown(output_fn, expanded_markdown):
    output_fn.parent.mkdir(exist_ok=True, parents=True)
    with open(output_fn, "w") as f:
        f.write(expanded_markdown)


def _get_raw_markdown(spec_file):
    with open(spec_file) as ifs:
        raw_markdown = ifs.read()
        raw_markdown = re.sub(r"\s\- ", " ", raw_markdown)
    return raw_markdown


class CustomMarkdown(mistune.Markdown):
    def output_paragraph(self):
        return self.renderer.paragraph(
            self.inline(self.token["text"]), self.token["text"]
        )
