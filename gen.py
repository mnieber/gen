import os
import parser
import sys

import mistune

import leap_mn
from config import config, install

leap_mn.install_all()


def get_blocks(raw_markdown):
    blockCollector = parser.BlockCollector(
        create_block=lambda name: parser.Block(name),
        create_line=parser.get_create_line(config.ittable_lut),
    )
    mistune.Markdown(renderer=blockCollector)(raw_markdown)
    return blockCollector.blocks


def main(gen_file):
    __import__("pudb").set_trace()
    with open(gen_file) as ifs:
        raw_markdown = ifs.read()

    blocks = get_blocks(raw_markdown)
    for block in blocks:
        parser.create_resources(block)

    for block in blocks:
        parser.update_resources(block)

    for block in blocks:
        print(block.describe())


def report(x):
    print(x)


if __name__ == "__main__":
    gen_file = "genspec.md"
    if not os.path.exists(gen_file):
        report("Genspec file not found: " + gen_file)
        sys.exit(1)

    try:
        main(gen_file)
    except Exception as e:
        report(f"Error: {e}")
