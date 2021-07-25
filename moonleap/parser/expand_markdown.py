from pathlib import Path

import mistune
from moonleap.context_manager import get_local_context_names


class Markdown(mistune.Markdown):
    def output_paragraph(self):
        return self.renderer.paragraph(
            self.inline(self.token["text"]), self.token["text"]
        )


def expand_markdown(spec_file, base_level=0, context_names=None):
    if context_names is None:
        context_names = []

    with open(spec_file) as ifs:
        raw_markdown = ifs.read()

    expander = BlockExpander(Path(spec_file).parent, base_level, context_names)
    Markdown(renderer=expander)(raw_markdown)
    return expander.output_text


def _update_local_context_names(raw, context_names, new_context_name):
    match = get_local_context_names(raw)

    local_context_names = match[1].replace(",", "").split() if match else []
    if new_context_name and new_context_name not in local_context_names:
        local_context_names.append(new_context_name)

    raw = raw.replace(match[0], "").strip() if match else raw
    new_context_names_str = ", ".join(
        context_names + [x for x in local_context_names if x not in context_names]
    )
    if new_context_names_str:
        raw = raw + f" {{{new_context_names_str}}}"
    return raw


def _update_external_link(sub_spec_link, raw):
    link_pattern = f"[{sub_spec_link[0]}]({sub_spec_link[1]})"
    raw = raw.replace(link_pattern, sub_spec_link[0])
    return raw


class BlockExpander(mistune.Renderer):
    def __init__(self, file_path, level, context_names):
        super().__init__(escape=True, hard_wrap=True)
        self.sub_spec_link = None
        self.output_text = ""
        self.base_level = level
        self.context_names = context_names
        self.file_path = file_path

    def header(self, text, level, raw):
        buffer = raw

        # Determine contents of the external link
        if self.sub_spec_link:
            sub_spec_context_name = Path(self.sub_spec_link[1]).stem
            if sub_spec_context_name in self.context_names:
                raise Exception("Every sub-spec file must have a unique name")
            sub_spec_content = expand_markdown(
                self.file_path / self.sub_spec_link[1],
                level,
                self.context_names + [sub_spec_context_name],
            )
        else:
            sub_spec_context_name = None
            sub_spec_content = None

        # Apply some transformations to the buffer
        if self.sub_spec_link:
            buffer = _update_external_link(self.sub_spec_link, buffer)
        buffer = _update_local_context_names(
            buffer, self.context_names, sub_spec_context_name
        )

        # Correct the Markdown indentation level
        self.output_text += "#" * (self.base_level + level) + " " + buffer + "\n" + "\n"

        # Add sub-spec content
        if sub_spec_content:
            self.output_text += sub_spec_content

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
