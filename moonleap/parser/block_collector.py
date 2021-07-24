import re

import mistune
import nltk
from moonleap.parser.block import Block
from moonleap.parser.expand_markdown import expand_markdown
from moonleap.parser.line import get_create_line
from moonleap.session import get_local_context_names

try:
    nltk.sent_tokenize("test")
except LookupError:
    nltk.download("punkt")


class FormatError(Exception):
    pass


def clean_text(text):
    result = text
    result = re.sub(r"<br\>", " ", result)
    result = re.sub(r"<[^<]+?>", "", result)
    return result


def clean_sentence(sentence):
    result = sentence
    for char in (",", ";", "\n"):
        result = result.replace(char, "")
    while result.endswith("."):
        result = result[:-1]
    return result


class BlockCollector(mistune.Renderer):
    def __init__(self, create_block, create_line):
        super().__init__(escape=True, hard_wrap=True)
        self.stack = []
        self.block = None
        self.blocks = []
        self.line = None
        self.create_block = create_block
        self.create_line = create_line

    @property
    def parent_block(self):
        return self.stack[-1] if self.stack else None

    def header(self, text, level, raw=None):
        # Read contexts from the header text and pass them to the
        # session object so that the correct moonleap packages are loaded
        # in order to process the header and its content
        buffer = raw
        matches = get_local_context_names(buffer)
        if matches:
            buffer = buffer.replace(matches[0], "").strip()
            local_context_names = [x.strip() for x in matches[1].split(",")]
        else:
            local_context_names = []

        while self.parent_block and self.parent_block.level >= level:
            self.stack.pop()

        self.block = self.create_block(
            buffer,
            level,
            self.parent_block,
            local_context_names,
        )
        self.stack.append(self.block)

        self.line = self.create_line(buffer, it_term=None)
        self.block.lines.append(self.line)
        self.blocks.append(self.block)
        return super().header(text, level, raw)

    def paragraph(self, text):
        if not self.block:
            raise FormatError("The spec file should start with a header")

        for sentence in nltk.sent_tokenize(clean_text(text)):
            self.line = self.create_line(
                clean_sentence(sentence), it_term=self.line.it_term
            )
            self.block.lines.append(self.line)
        return super().paragraph(text)


def create_block(name, level, parent_block, context_names):
    inherited_context_names = (
        parent_block.context_names if parent_block else ["default"]
    )
    block = Block(
        name,
        level,
        [x for x in inherited_context_names if x not in context_names] + context_names,
    )
    block.link(parent_block)
    return block


def get_blocks(spec_file):
    blockCollector = BlockCollector(
        create_block=create_block,
        create_line=get_create_line(),
    )
    expanded_markdown = expand_markdown(spec_file)
    mistune.Markdown(renderer=blockCollector)(expanded_markdown)
    return blockCollector.blocks
