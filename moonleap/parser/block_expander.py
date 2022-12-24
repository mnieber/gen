from pathlib import Path

import mistune

from moonleap.scope_manager import get_local_scope_names


def _update_local_scope_names(raw, scope_names, new_scope_name):
    match = get_local_scope_names(raw)

    local_scope_names = match[1].replace(",", "").split() if match else []
    if new_scope_name and new_scope_name not in local_scope_names:
        local_scope_names.append(new_scope_name)

    raw = raw.replace(match[0], "").strip() if match else raw
    new_scope_names_str = ", ".join(
        scope_names + [x for x in local_scope_names if x not in scope_names]
    )
    if new_scope_names_str:
        raw = raw + f" {{{new_scope_names_str}}}"
    return raw


def _update_external_link(sub_spec_link, raw):
    link_pattern = f"[{sub_spec_link[0]}]({sub_spec_link[1]})"
    raw = raw.replace(link_pattern, sub_spec_link[0])
    return raw


class BlockExpander(mistune.Renderer):
    def __init__(self, file_path, level, scope_names):
        super().__init__(escape=True, hard_wrap=True)
        self.sub_spec_link = None
        self.output_text = ""
        self.base_level = level
        self.scope_names = scope_names
        self.file_path = file_path

    def header(self, text, level, raw):
        from moonleap.parser.expand_markdown import expand_markdown

        buffer = raw

        # Determine contents of the external link
        if self.sub_spec_link:
            sub_spec_scope_name = Path(self.sub_spec_link[1]).stem
            if sub_spec_scope_name in self.scope_names:
                raise Exception("Every sub-spec file must have a unique name")
            sub_spec_content = expand_markdown(
                self.file_path / self.sub_spec_link[1],
                base_level=level,
                scope_names=self.scope_names + [sub_spec_scope_name],
            )
        else:
            sub_spec_scope_name = None
            sub_spec_content = None

        # Apply some transformations to the buffer
        if self.sub_spec_link:
            buffer = _update_external_link(self.sub_spec_link, buffer)
        buffer = _update_local_scope_names(
            buffer, self.scope_names, sub_spec_scope_name
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
