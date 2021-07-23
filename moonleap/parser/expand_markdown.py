import re
from pathlib import Path

import mistune


class Markdown(mistune.Markdown):
    def output_paragraph(self):
        return self.renderer.paragraph(
            self.inline(self.token["text"]), self.token["text"]
        )


def expand_markdown(spec_file, base_level=0, contexts=None):
    if contexts == None:
        contexts = []

    with open(spec_file) as ifs:
        raw_markdown = ifs.read()

    expander = BlockExpander(Path(spec_file).parent, base_level, contexts)
    Markdown(renderer=expander)(raw_markdown)
    return expander.output_text


def _update_local_contexts(raw, contexts):
    match = _get_local_contexts(raw)
    local_contexts = match[1].replace(",", "").split() if match else []
    raw = raw.replace(match[0], "").strip() if match else raw
    new_contexts_str = ", ".join(
        contexts + [x for x in local_contexts if x not in contexts]
    )
    if new_contexts_str:
        raw = raw + f" {{{new_contexts_str}}}"
    return raw


def _get_local_contexts(raw):
    contexts_pattern = r"(\{(((\s)*(\w)+(\,)?)+)\})"
    matches = re.findall(contexts_pattern, raw, re.MULTILINE)
    return matches[0] if matches else None


def _update_external_link(sub_spec_link, raw):
    link_pattern = f"[{sub_spec_link[0]}]({sub_spec_link[1]})"
    raw = raw.replace(link_pattern, sub_spec_link[0])
    return raw


class BlockExpander(mistune.Renderer):
    def __init__(self, file_path, level, contexts):
        super().__init__(escape=True, hard_wrap=True)
        self.sub_spec_link = None
        self.output_text = ""
        self.base_level = level
        self.contexts = contexts
        self.file_path = file_path

    def header(self, text, level, raw):
        # Apply some transformations to the raw text
        if self.sub_spec_link:
            raw = _update_external_link(self.sub_spec_link, raw)
        raw = _update_local_contexts(raw, self.contexts)

        # Correct the Markdown indentation level
        self.output_text += "#" * (self.base_level + level) + " " + raw + "\n" + "\n"

        # Add contents of the external link
        if self.sub_spec_link:
            new_context = Path(self.sub_spec_link[1]).stem
            if new_context in self.contexts:
                raise Exception("Every sub-spec file must have a unique name")
            self.output_text += expand_markdown(
                self.file_path / self.sub_spec_link[1],
                level,
                self.contexts + [new_context],
            )

        # Reset the sub-spec link that was already consumed
        self.sub_spec_link = None

        return super().header(text, level, raw)

    def paragraph(self, text, raw):
        self.sub_spec_link = None
        self.output_text += raw + "\n" + "\n"
        return super().paragraph(text)

    def link(self, link, title, content):
        if Path(link).suffix == ".md":
            self.sub_spec_link = (content, link)
        return super().link(link, title, content)
