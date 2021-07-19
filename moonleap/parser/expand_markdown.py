from pathlib import Path

import mistune


class Markdown(mistune.Markdown):
    def output_paragraph(self):
        return self.renderer.paragraph(
            self.inline(self.token["text"]), self.token["text"]
        )


def expand_markdown(spec_file, base_level=0):
    with open(spec_file) as ifs:
        raw_markdown = ifs.read()

    expander = BlockExpander(Path(spec_file).parent, base_level)
    Markdown(renderer=expander)(raw_markdown)
    return expander.output_text


class BlockExpander(mistune.Renderer):
    def __init__(self, file_path, level):
        super().__init__(escape=True, hard_wrap=True)
        self.sub_spec_link = None
        self.output_text = ""
        self.base_level = level
        self.file_path = file_path

    def header(self, text, level, raw):
        if self.sub_spec_link:
            raw = raw.replace(
                f"[{self.sub_spec_link[0]}]({self.sub_spec_link[1]})",
                self.sub_spec_link[0],
            )

        self.output_text += "#" * (self.base_level + level) + " " + raw + "\n" + "\n"

        if self.sub_spec_link:
            self.output_text += expand_markdown(
                self.file_path / self.sub_spec_link[1], level
            )

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
