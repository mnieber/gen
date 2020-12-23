from parser import Block

import mistune


class FormatError(Exception):
    pass


class BlockCollector(mistune.Renderer):
    def __init__(self, ittable_lut, create_line):
        super().__init__(escape=True, hard_wrap=True)
        self.ittable_lut = ittable_lut
        self.block = None
        self.blocks = []
        self.line = None
        self.create_line = create_line

    def header(self, text, level, raw=None):
        if level <= 2:
            self.block = Block(text)
            self.line = self.create_line(text, it=None)
            self.block.lines.append(self.line)
            self.blocks.append(self.block)
        return super().header(text, level, raw)

    def paragraph(self, text):
        if not self.block:
            raise FormatError("The spec file should start with a header")

        for line_text in text.replace(",", "").replace(";", "").split("."):
            self.line = self.create_line(
                line_text, it=self.line.next_it(self.ittable_lut)
            )
            self.block.lines.append(self.line)
        return super().paragraph(text)
